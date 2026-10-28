# Raspberry Pi hardware setup

## Recommended hardware

See the complete [bill of materials](PARTS.md), [GPIO wiring](WIRING.md), and
[assembly guide](ASSEMBLY.md). The recommended core is a Raspberry Pi 5,
Camera Module 3, physical interlock, Home Assistant MQTT broker, and one smart
bulb for initial commissioning.

## Camera software

Use 64-bit Raspberry Pi OS Bookworm or newer. Picamera2 is part of the modern
`libcamera`/`rpicam` stack; do not follow legacy `raspistill` or `picamera`
tutorials.

```bash
sudo apt update
sudo apt install -y python3-picamera2 python3-opencv python3-venv
rpicam-hello
```

Create a virtual environment that can see system packages, then install the
remaining dependencies:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[camera,mqtt,hardware]'
```

Download Google's MediaPipe `gesture_recognizer.task` model from the official
MediaPipe Gesture Recognizer documentation and place it in `models/`. Model
files are not committed because their versions and licenses must remain clear.

## Commissioning order

1. Run the recorded simulation and tests.
2. Run camera mode without `--live` and inspect dry-run logs.
3. Test each gesture under bright, dim, and backlit conditions.
4. Configure one smart bulb in `default.json`.
5. Assemble and verify the GPIO interlock. Live mode always requires it.
6. Add the Home Assistant MQTT automation from `home-assistant.yaml`.
7. Only then run camera mode with `--live`.

```bash
pi-gesture-home camera --model models/gesture_recognizer.task
pi-gesture-home camera --model models/gesture_recognizer.task --live
```

MQTT credentials should be supplied outside the repository. Never commit them
to `default.json`:

```bash
export PIGESTURE_MQTT_USERNAME='gesture-controller'
export PIGESTURE_MQTT_PASSWORD='replace-with-your-password'
```
