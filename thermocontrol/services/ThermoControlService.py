import logging
import time

from thermocontrol.dto import Context
from thermocontrol.services.RpiService import RpiService
from thermocontrol.services.TemperatureService import TemperatureService

class ThermoControlService:
    def __init__(self, context: Context):
        logging.info(f"Initializing ThermoControlService with context: {context}")
        self.context = context
        self.temperature_service = TemperatureService(context)
        self.rpi_service = RpiService(context)

        self.thermo_control_thread_is_running = True
        self._run_thermo_control()

    def _run_thermo_control(self):
        while self.thermo_control_thread_is_running:
            try:
                time.sleep(self.context.thermo_check_interval)
                self._ai_module_fan_thermocontrol()
            except KeyboardInterrupt:
                self.thermo_control_thread_is_running = False
            except Exception as e:
                logging.error(f"Error occurred during AI module temperature control: {e}")

    def _ai_module_fan_thermocontrol(self) -> None:
        temperature = self.temperature_service.get_temperature_ai_module()
        logging.debug(f"AI module temperature: {temperature} >< {self.context.ai_temperature_threshold}")
        self.rpi_service.ai_module_fan(temperature >= self.context.ai_temperature_threshold)

    def __close__(self) -> None:
        self.ai_thermo_control_thread_is_running=False
        self.rpi_service.__close__()
        logging.info("Closing ThermoControlService")