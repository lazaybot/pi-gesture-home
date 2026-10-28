# Physical assembly and commissioning

## 1. Prepare the Raspberry Pi

1. Do not connect USB-C power yet.
2. Discharge static before handling the camera or Pi.
3. Insert the microSD card after flashing 64-bit Raspberry Pi OS.
4. Connect the Pi 5 camera cable before installing the Active Cooler; the
   cooler makes the CAM/DISP connectors harder to reach.
5. Install the Active Cooler according to its supplied instructions.
6. Mount the Pi in a ventilated case that leaves the GPIO header accessible.

## 2. Connect Camera Module 3

1. With the Pi unpowered, open the latch on CAM/DISP0 or CAM/DISP1.
2. Insert the mini 22-pin end straight into the Pi connector. The exposed metal
   contacts face away from the connector flap.
3. Close the latch without forcing it.
4. At the camera, open its connector and insert the standard 15-pin end with
   the contacts facing toward the camera board and away from the flap.
5. Close the camera latch and ensure the cable is even, not angled or sharply
   folded.
6. Mount the camera 1.5–2.5 m from the gesture area, near eye level, with the
   lens aimed away from windows that cause backlighting.

## 3. Build the interlock circuit

1. Follow [WIRING.md](WIRING.md) on a breadboard while power remains off.
2. Keep the maintained switch outside the enclosure and easy to reach.
3. Place the green LED where it is visible from the gesture area.
4. Run every check in the pre-power checklist.
5. For a permanent build, solder and insulate the connections only after the
   breadboard prototype passes all tests.

## 4. Test the camera and GPIO separately

Power the Pi with the official supply and run:

```bash
pinout
rpicam-hello
```

Stop if the camera is missing, the Pi reports undervoltage, or any component
gets warm. Recheck the camera-cable orientation and power supply.

After installing the project and `gpiozero`, test the interlock:

```bash
python -c "from pi_gesture_home.interlock import GpioInterlock; x=GpioInterlock(); print('enabled=', x.enabled); x.set_armed(True); input('Press Enter to exit: '); x.close()"
```

The output must be `enabled=False` with the switch open and `enabled=True` with
it closed. The LED may illuminate only when both armed and enabled.

## 5. Install and test the application

Follow [HARDWARE_SETUP.md](HARDWARE_SETUP.md), then run the recorded simulation
before starting the camera. Test camera mode without `--live` for at least 50
gesture attempts under different lighting conditions.

Record:

- intended gestures correctly detected;
- missed gestures;
- incorrect gestures;
- activations when no command was intended;
- camera-to-command latency.

Do not enable MQTT control if any no-intent test produces a command.

## 6. Connect Home Assistant

1. Create a dedicated MQTT account with access only to
   `pi-gesture-home/command`.
2. Change the example entity IDs to one test bulb.
3. add and review [home-assistant.yaml](home-assistant.yaml).
4. Keep the physical switch open and start camera mode.
5. Confirm gestures appear only as blocked or dry-run events.
6. Close the switch, arm with an open palm, and test light-on once.
7. Verify the bulb state in Home Assistant, then open the switch again.

## 7. Final mounting

Secure the camera and Pi so neither can move during normal use. A changed camera
angle invalidates motion thresholds and requires retesting. Cover the breadboard
or soldered board with a non-conductive enclosure, provide strain relief for the
camera cable, and label the enable switch positions clearly.
