import logging
import threading
import time

from dto import Context
from services.RpiService import RpiService
from services.TemperatureService import TemperatureService

class ThermoControlService:
    def __init__(self, context: Context):
        self.context = context
        self.temperature_service = TemperatureService(context)
        self.rpi_service = RpiService(context)

        self.ai_thermo_control_thread_is_running = True
        self.ai_thermo_control_thread = threading.Thread(target=self._run_ai_module_thermo_control, daemon=True)
        self.ai_thermo_control_thread.start()

    def _run_ai_module_thermo_control(self):
        while self.ai_thermo_control_thread_is_running:
            try:
                temperature = self.temperature_service.get_temperature_ai_module()
                self.rpi_service.ai_module_fan(temperature >= self.context.ai_temperature_threshold)
                time.sleep(self.context.ai_thermo_control_interval)
            except KeyboardInterrupt:
                self.ai_thermo_control_thread_is_running = False
            except Exception as e:
                logging.error(f"Error occurred during AI module temperature control: {e}")

    def __close__(self) -> None:
        self.ai_thermo_control_thread_is_running=False
        self.ai_thermo_control_thread.join()
        logging.info("Closing ThermoControlService")