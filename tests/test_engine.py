import json
import unittest
from pathlib import Path

from pi_gesture_home.config import load_config
from pi_gesture_home.engine import GestureEngine
from pi_gesture_home.models import Command, Detection


ROOT = Path(__file__).resolve().parents[1]


def detection(t, pose, x=0.5, y=0.5, confidence=0.95):
    return Detection(t, pose, confidence, x, y)


class GestureEngineTests(unittest.TestCase):
    def test_open_palm_then_thumbs_up_turns_light_on(self):
        engine = GestureEngine()
        frames = [
            detection(0, "open_palm"), detection(0.4, "open_palm"), detection(0.85, "open_palm"),
            detection(1.0, "thumbs_up"), detection(1.25, "thumbs_up"), detection(1.5, "thumbs_up"),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertEqual([event.command for event in events if event.command], [Command.LIGHT_ON])

    def test_command_without_activation_is_ignored(self):
        engine = GestureEngine()
        frames = [detection(0, "thumbs_up"), detection(0.5, "thumbs_up"), detection(1, "thumbs_up")]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertFalse(any(event.command for event in events))

    def test_low_confidence_breaks_confirmation(self):
        engine = GestureEngine()
        frames = [
            detection(0, "open_palm"), detection(0.5, "open_palm", confidence=0.4),
            detection(1.0, "open_palm"),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertFalse(any(event.kind == "armed" for event in events))

    def test_pointing_swipe_right_brightens_after_activation(self):
        engine = GestureEngine()
        frames = [
            detection(0, "open_palm"), detection(0.4, "open_palm"), detection(0.85, "open_palm"),
            detection(1.0, "pointing", x=0.20), detection(1.3, "pointing", x=0.35),
            detection(1.65, "pointing", x=0.52),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertEqual([event.command for event in events if event.command], [Command.BRIGHTER])

    def test_pointing_swipe_left_dims_after_activation(self):
        engine = GestureEngine()
        frames = [
            detection(0, "open_palm"), detection(0.4, "open_palm"), detection(0.85, "open_palm"),
            detection(1.0, "pointing", x=0.75), detection(1.3, "pointing", x=0.60),
            detection(1.65, "pointing", x=0.43),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertEqual([event.command for event in events if event.command], [Command.DIMMER])

    def test_armed_state_times_out(self):
        engine = GestureEngine(armed_timeout_seconds=2.0)
        frames = [
            detection(0, "open_palm"), detection(0.4, "open_palm"), detection(0.85, "open_palm"),
            detection(3.0, "thumbs_up"), detection(3.6, "thumbs_up"),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertTrue(any(event.kind == "disarmed" for event in events))
        self.assertFalse(any(event.command for event in events))

    def test_cooldown_prevents_duplicate_command(self):
        engine = GestureEngine()
        frames = [
            detection(0, "open_palm"), detection(0.4, "open_palm"), detection(0.85, "open_palm"),
            detection(1.0, "thumbs_up"), detection(1.5, "thumbs_up"),
            detection(1.7, "open_palm"), detection(2.6, "open_palm"),
            detection(2.7, "thumbs_up"), detection(3.2, "thumbs_up"),
        ]
        events = [event for frame in frames for event in engine.update(frame)]
        self.assertEqual(sum(event.command == Command.LIGHT_ON for event in events), 1)

    def test_configuration_rejects_lock_domain(self):
        raw = json.loads((ROOT / "pi_gesture_home/config/default.json").read_text())
        raw["gestures"]["light_on"]["entity_id"] = "lock.front_door"
        path = ROOT / "outputs/unsafe-test.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(raw))
        with self.assertRaisesRegex(ValueError, "unsafe or unsupported"):
            load_config(path)


if __name__ == "__main__":
    unittest.main()
