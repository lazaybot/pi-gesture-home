# Bill of materials

This list builds one reliable Raspberry Pi 5 camera controller. Home Assistant
may run on this Pi or an existing server.

## Required computing and camera parts

| Qty | Part | Recommended specification | Purpose |
| ---: | --- | --- | --- |
| 1 | Raspberry Pi 5 | 4 GB or 8 GB | Local camera inference and MQTT client |
| 1 | Official USB-C power supply | Raspberry Pi 27 W, 5.1 V/5 A | Stable Pi 5 and camera power |
| 1 | microSD card | 32 GB or larger, A2-rated | Raspberry Pi OS and application |
| 1 | Active Cooler | Official Pi 5 Active Cooler | Prevents inference throttling |
| 1 | Camera Module 3 | Standard or Wide, visible-light model | Autofocus hand capture |
| 1 | Camera cable | Standard 15-pin to mini 22-pin, 200–300 mm | Required for Camera Module 3 to Pi 5 |
| 1 | Pi 5 case or mounting plate | Must clear CSI cable and GPIO header | Mechanical protection |
| 1 | Camera mount | Adjustable wall/desk mount for 25 × 24 mm module | Stable viewing angle |

The normal Camera Module 3 package may contain a standard-to-standard cable.
Pi 5 uses a mini 22-pin CAM/DISP connector, so verify that the standard-to-mini
cable is included or purchase it separately.

## Interlock and indicator parts

| Qty | Part | Value/type | Purpose |
| ---: | --- | --- | --- |
| 1 | Maintained toggle or rocker switch | SPST, low-voltage | Physical live-control enable |
| 1 | LED | Diffused green, 3 mm or 5 mm | Armed-state indicator |
| 1 | Resistor | 330 ohm, 1/4 W | Limits LED current |
| 1 | Resistor | 10 kilohm, 1/4 W | External pull-up for fail-open input |
| 1 | Solderless breadboard | Half-size or smaller | Prototype wiring |
| 6 | Female-to-male jumper wires | 2.54 mm | Pi-to-breadboard connections |
| 1 | Small enclosure | Non-conductive | Covers exposed wiring |

## Home-control parts

| Qty | Part | Requirement |
| ---: | --- | --- |
| 1 | Home Assistant installation | Existing server, Home Assistant Green, or Pi installation |
| 1 | MQTT broker | Mosquitto add-on or equivalent |
| 1+ | Smart bulb | Home Assistant-compatible; start with one lamp |

Do not commission the first version with locks, garage doors, heaters, ovens,
alarms, blinds near people, or generic smart plugs attached to heating loads.

## Tools

- Small Phillips screwdriver
- ESD strap, or a grounded metal surface to discharge static
- Needle-nose pliers
- Multimeter for continuity and voltage checks
- Double-sided foam tape or M2 hardware for the camera mount
- Optional soldering iron and heat-shrink tubing for the final enclosure
