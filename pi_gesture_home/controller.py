"""Dry-run and MQTT Home Assistant controllers."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .models import Command


class DryRunController:
    def __init__(self, mappings: dict, log_path: str | Path | None = None) -> None:
        self.mappings = mappings
        self.log_path = Path(log_path) if log_path else None
        self.events: list[dict] = []

    def execute(self, command: Command) -> dict:
        if command == Command.CANCEL:
            result = {"command": command.value, "status": "cancelled", "mode": "dry-run"}
        else:
            mapping = self.mappings[command.value]
            result = {"command": command.value, "status": "simulated", "mode": "dry-run", **mapping}
        self.events.append(result)
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "events": self.events,
            }
            self.log_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        return result


class HomeAssistantMqttController:
    """Publish commands for an MQTT automation; defaults to no retained messages."""

    def __init__(self, mappings: dict, host: str, port: int = 1883, username: str | None = None, password: str | None = None) -> None:
        try:
            import paho.mqtt.client as mqtt
        except ImportError as error:
            raise RuntimeError("install the MQTT extra: pip install -e '.[mqtt]'") from error
        self.mappings = mappings
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        if username:
            self.client.username_pw_set(username, password)
        self.client.connect(host, port, 30)
        self.client.loop_start()

    def execute(self, command: Command) -> dict:
        if command == Command.CANCEL:
            return {"command": command.value, "status": "cancelled"}
        mapping = self.mappings[command.value]
        topic = "pi-gesture-home/command"
        payload = json.dumps({"command": command.value, **mapping})
        info = self.client.publish(topic, payload, qos=1, retain=False)
        info.wait_for_publish(timeout=2.0)
        if info.rc != 0:
            raise RuntimeError(f"MQTT publish failed with code {info.rc}")
        return {"command": command.value, "status": "published", "topic": topic}
