"""Physical live-mode interlock and status indicator for Raspberry Pi GPIO."""

from __future__ import annotations


class GpioInterlock:
    """Fail-open maintained switch on GPIO17 and armed LED on GPIO27."""

    def __init__(self, enable_pin: int = 17, led_pin: int = 27) -> None:
        try:
            from gpiozero import Button, LED
        except ImportError as error:
            raise RuntimeError("install the hardware extra: pip install -e '.[hardware]'") from error
        self.switch = Button(enable_pin, pull_up=True, bounce_time=0.05)
        self.led = LED(led_pin, initial_value=False)

    @property
    def enabled(self) -> bool:
        return bool(self.switch.is_pressed)

    def set_armed(self, armed: bool) -> None:
        if armed and self.enabled:
            self.led.on()
        else:
            self.led.off()

    def close(self) -> None:
        self.led.off()
        self.switch.close()
        self.led.close()
