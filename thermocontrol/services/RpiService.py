from dto import Context
from gpiozero import OutputDevice


class RpiService:
    def __init__(self, context: Context):
        self.context = context
        self.fan = OutputDevice(context.ai_thermo_control_gpio_pin)

    def ai_module_fan(self, enable: bool):
        self.fan.on() if enable else self.fan.off()
