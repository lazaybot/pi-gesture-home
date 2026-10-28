# GPIO wiring

Raspberry Pi GPIO uses **3.3 V logic and is not 5 V tolerant**. Disconnect USB-C
power before changing wiring. Numbering below includes both BCM/GPIO names and
physical header pin numbers.

## Pin assignment

| Function | GPIO name | Physical pin |
| --- | --- | ---: |
| Enable-switch input | GPIO17 | 11 |
| Armed LED output | GPIO27 | 13 |
| 3.3 V pull-up supply | 3V3 | 1 |
| Switch ground | GND | 9 |
| LED ground | GND | 14 |

## Connection diagram

```text
Physical pin 1 (3.3 V) ---- 10 kΩ ----+
                                      |
Physical pin 11 (GPIO17) -------------+---- maintained switch ---- pin 9 (GND)

Physical pin 13 (GPIO27) ---- 330 Ω ---- LED anode (+)
                                           LED cathode (-) ---- pin 14 (GND)
```

The switch is fail-open: when the wire is disconnected or the switch is open,
GPIO17 remains high and live commands are blocked. Closing the switch pulls
GPIO17 to ground; GPIO Zero reports that as pressed/enabled.

For the LED, the longer lead is normally the anode. Confirm polarity using the
component datasheet or a multimeter diode-test function. Never omit the 330-ohm
series resistor.

## Pre-power checks

1. Confirm no connection exists between a 5 V pin and either GPIO.
2. With power disconnected and the switch open, check that GPIO17 is connected
   to 3.3 V only through the 10-kilohm resistor.
3. Close the switch and confirm continuity between GPIO17 and ground.
4. Confirm the LED path includes the 330-ohm resistor.
5. Inspect for loose strands or jumpers that could bridge adjacent pins.

The official Raspberry Pi `pinout` command should show GPIO17 at physical pin
11 and GPIO27 at physical pin 13 before you connect the circuit.
