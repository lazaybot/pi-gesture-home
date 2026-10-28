# PiGesture Home

Local Raspberry Pi camera gesture control for low-risk Home Assistant devices.

PiGesture Home recognizes a deliberate activation gesture followed by a held
pose or hand motion. It can control lights, fans, and media players through
MQTT. Camera frames stay on the Raspberry Pi and are not recorded by default.

## Why this design

A single-frame gesture is too easy to trigger accidentally. This project uses:

- an open-palm activation held for 0.8 seconds;
- multi-frame confidence checks;
- a separate command gesture or directional motion;
- a cooldown after every command;
- an allowlist that rejects locks, covers, climate, alarms, and switches;
- dry-run mode as the default.

## Quick test without hardware

```bash
python -m pi_gesture_home.cli simulate examples/light_on.json
python -m unittest discover -s tests -v
```

Expected result: the example arms once and simulates one `light_on` command.

## Gesture map

| Sequence | Command |
| --- | --- |
| Open palm, then thumbs up | Light on |
| Open palm, then thumbs down | Light off |
| Open palm, then point and swipe right | Brighter |
| Open palm, then point and swipe left | Dimmer |
| Open palm, then point and swipe up | Next media track |
| Open palm, then hold a fist | Cancel |

See [HARDWARE_SETUP.md](HARDWARE_SETUP.md) for Raspberry Pi installation and
[SAFETY.md](SAFETY.md) before connecting real devices.

Complete hardware documentation:

- [Bill of materials](PARTS.md)
- [GPIO wiring and pre-power checks](WIRING.md)
- [Step-by-step assembly and commissioning](ASSEMBLY.md)

## Status

The deterministic gesture engine, safety allowlist, simulation CLI, and tests
are complete. Camera and MQTT adapters are implemented but have not been tested
on physical Raspberry Pi or Home Assistant hardware in this environment.

## License and attribution

Apache-2.0. The implementation is original and uses the public APIs of
Picamera2, MediaPipe, Paho MQTT, and Home Assistant. Those dependencies retain
their own licenses and trademarks.

References: [Raspberry Pi camera software](https://www.raspberrypi.com/documentation/computers/camera_software.html),
[Google MediaPipe Raspberry Pi hand example](https://github.com/google-ai-edge/mediapipe-samples/tree/main/examples/hand_landmarker/raspberry_pi),
and [Home Assistant MQTT](https://www.home-assistant.io/integrations/mqtt/).
