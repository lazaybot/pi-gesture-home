# Safety boundary

Computer vision is probabilistic. A high confidence score does not guarantee a
correct command.

This release permits only `light`, `fan`, and `media_player` Home Assistant
domains. It rejects locks and intentionally excludes garage doors, ovens,
heaters, alarms, climate control, and general smart plugs.

Required safeguards for a real installation:

- retain the activation gesture, multi-frame confirmation, and cooldown;
- provide the physical fail-open controller switch; live mode requires it;
- indicate armed state with a visible LED;
- keep manual controls available;
- use MQTT state feedback instead of assuming a command succeeded;
- collect false-positive measurements without saving video;
- never position the camera where private spaces are recorded;
- keep processing local and firewall the Pi from unsolicited internet access.

The system is convenience automation, not a safety controller or security
system.
