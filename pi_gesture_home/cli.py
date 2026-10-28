"""Run recorded simulations or the optional Raspberry Pi camera adapter."""

from __future__ import annotations

import argparse
import json
import os
from importlib.resources import files

from .config import load_config
from .controller import DryRunController, HomeAssistantMqttController
from .engine import GestureEngine
from .models import Detection


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Local gesture control for Home Assistant")
    result.add_argument("--config", default=str(files("pi_gesture_home").joinpath("config/default.json")))
    result.add_argument("--log", default="outputs/events.json")
    sub = result.add_subparsers(dest="mode", required=True)
    simulate = sub.add_parser("simulate")
    simulate.add_argument("detections", help="JSON list of recorded detections")
    camera = sub.add_parser("camera")
    camera.add_argument("--model", required=True, help="MediaPipe gesture_recognizer.task")
    camera.add_argument("--live", action="store_true", help="publish to MQTT instead of dry run")
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        config = load_config(args.config)
        engine = GestureEngine(**config["safety"])
        if args.mode == "camera" and args.live:
            from .interlock import GpioInterlock

            mqtt = config["mqtt"]
            interlock = GpioInterlock()
            controller = HomeAssistantMqttController(
                config["gestures"],
                mqtt["host"],
                mqtt.get("port", 1883),
                os.environ.get("PIGESTURE_MQTT_USERNAME"),
                os.environ.get("PIGESTURE_MQTT_PASSWORD"),
            )
        else:
            interlock = None
            controller = DryRunController(config["gestures"], args.log)

        if args.mode == "simulate":
            raw = json.loads(open(args.detections, encoding="utf-8").read())
            source = (Detection(**item) for item in raw)
        else:
            from .vision import PiCameraGestureSource

            camera = PiCameraGestureSource(args.model)
            source = camera.detections()

        for detection in source:
            for event in engine.update(detection):
                print(f"{event.timestamp:.2f} {event.kind}: {event.detail}")
                if interlock and event.kind == "armed":
                    interlock.set_armed(True)
                if event.command is not None:
                    if interlock and not interlock.enabled:
                        print(json.dumps({"command": event.command.value, "status": "blocked-by-interlock"}))
                    else:
                        print(json.dumps(controller.execute(event.command), sort_keys=True))
                    if interlock:
                        interlock.set_armed(False)
                elif interlock and event.kind == "disarmed":
                    interlock.set_armed(False)
    except (OSError, ValueError, KeyError, RuntimeError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
