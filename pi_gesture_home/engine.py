"""Temporal confirmation state machine that rejects single-frame gestures."""

from __future__ import annotations

from collections import deque

from .models import Command, Detection, EngineEvent


class GestureEngine:
    """Turn confirmed pose and motion sequences into bounded commands.

    An open palm must be held to arm the engine. A command then needs either a
    held pose or a deliberate swipe. After a command, the engine disarms and
    enters a cooldown so one motion cannot fire twice.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.78,
        activation_seconds: float = 0.8,
        command_seconds: float = 0.45,
        armed_timeout_seconds: float = 4.0,
        cooldown_seconds: float = 2.0,
        swipe_distance: float = 0.28,
        max_history_seconds: float = 1.2,
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.activation_seconds = activation_seconds
        self.command_seconds = command_seconds
        self.armed_timeout_seconds = armed_timeout_seconds
        self.cooldown_seconds = cooldown_seconds
        self.swipe_distance = swipe_distance
        self.max_history_seconds = max_history_seconds
        self._history: deque[Detection] = deque()
        self._armed_at: float | None = None
        self._cooldown_until = 0.0

    @property
    def armed(self) -> bool:
        return self._armed_at is not None

    def update(self, detection: Detection) -> list[EngineEvent]:
        events: list[EngineEvent] = []
        if detection.confidence < self.confidence_threshold:
            self._history.clear()
            return events

        while self._history and detection.timestamp - self._history[0].timestamp > self.max_history_seconds:
            self._history.popleft()
        self._history.append(detection)

        if self._armed_at is not None and detection.timestamp - self._armed_at > self.armed_timeout_seconds:
            self._armed_at = None
            self._history.clear()
            return [EngineEvent(detection.timestamp, "disarmed", "activation timed out")]

        if detection.timestamp < self._cooldown_until:
            return events

        if not self.armed:
            if self._held("open_palm", self.activation_seconds):
                self._armed_at = detection.timestamp
                self._history.clear()
                events.append(EngineEvent(detection.timestamp, "armed", "open palm confirmed"))
            return events

        command = self._command()
        if command is not None:
            events.append(EngineEvent(detection.timestamp, "command", command.value, command))
            self._armed_at = None
            self._cooldown_until = detection.timestamp + self.cooldown_seconds
            self._history.clear()
        return events

    def _held(self, pose: str, duration: float) -> bool:
        matching = [item for item in self._history if item.pose == pose]
        if len(matching) < 2 or len(matching) != len(self._history):
            return False
        return matching[-1].timestamp - matching[0].timestamp >= duration

    def _command(self) -> Command | None:
        if self._held("fist", self.command_seconds):
            return Command.CANCEL
        if self._held("thumbs_up", self.command_seconds):
            return Command.LIGHT_ON
        if self._held("thumbs_down", self.command_seconds):
            return Command.LIGHT_OFF
        if len(self._history) < 3:
            return None
        start, end = self._history[0], self._history[-1]
        duration = end.timestamp - start.timestamp
        if duration <= 0 or duration > self.max_history_seconds:
            return None
        dx, dy = end.palm_x - start.palm_x, end.palm_y - start.palm_y
        stable_pose = all(item.pose == "pointing" for item in self._history)
        if not stable_pose:
            return None
        if abs(dx) >= self.swipe_distance and abs(dx) > abs(dy) * 1.5:
            return Command.BRIGHTER if dx > 0 else Command.DIMMER
        if dy <= -self.swipe_distance and abs(dy) > abs(dx) * 1.5:
            return Command.MEDIA_NEXT
        return None
