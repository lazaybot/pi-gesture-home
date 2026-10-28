import sys
import types
import unittest


class FakeButton:
    def __init__(self, pin, pull_up, bounce_time):
        self.pin = pin
        self.pull_up = pull_up
        self.bounce_time = bounce_time
        self.is_pressed = False
        self.closed = False

    def close(self):
        self.closed = True


class FakeLED:
    def __init__(self, pin, initial_value):
        self.pin = pin
        self.value = initial_value
        self.closed = False

    def on(self):
        self.value = True

    def off(self):
        self.value = False

    def close(self):
        self.closed = True


class InterlockTests(unittest.TestCase):
    def setUp(self):
        self.previous = sys.modules.get("gpiozero")
        sys.modules["gpiozero"] = types.SimpleNamespace(Button=FakeButton, LED=FakeLED)

    def tearDown(self):
        if self.previous is None:
            sys.modules.pop("gpiozero", None)
        else:
            sys.modules["gpiozero"] = self.previous

    def test_open_switch_keeps_armed_led_off(self):
        from pi_gesture_home.interlock import GpioInterlock

        interlock = GpioInterlock()
        interlock.set_armed(True)
        self.assertFalse(interlock.enabled)
        self.assertFalse(interlock.led.value)

    def test_closed_switch_allows_armed_led(self):
        from pi_gesture_home.interlock import GpioInterlock

        interlock = GpioInterlock()
        interlock.switch.is_pressed = True
        interlock.set_armed(True)
        self.assertTrue(interlock.enabled)
        self.assertTrue(interlock.led.value)


if __name__ == "__main__":
    unittest.main()
