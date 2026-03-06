from thermocontrol.application.services.thermo_control_service import ThermoControlService
from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.rpi_service_interface import RpiServiceInterface
from thermocontrol.domain.services.temperature_service_interface import TemperatureServiceInterface


class FakeTemperatureService(TemperatureServiceInterface):
    def __init__(self, temperature: float):
        self.temperature = temperature

    def get_temperature_ai_module(self) -> float:
        return self.temperature


class FakeRpiService(RpiServiceInterface):
    def __init__(self):
        self.last_toggle = None
        self.closed = False

    def toggle_ai_cooler(self, enable: bool) -> None:
        self.last_toggle = enable

    def close(self) -> None:
        self.closed = True


def test_control_ai_module_fan_once_turns_on_fan_at_or_above_threshold() -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService(55.0),
        rpi_service=FakeRpiService(),
    )

    service.control_ai_module_fan_once()

    assert service.rpi_service.last_toggle is True


def test_control_ai_module_fan_once_turns_off_fan_below_threshold() -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService(54.9),
        rpi_service=FakeRpiService(),
    )

    service.control_ai_module_fan_once()

    assert service.rpi_service.last_toggle is False


def test_close_stops_loop_and_closes_rpi_service() -> None:
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=ContextEntity(),
        temperature_service=FakeTemperatureService(0.0),
        rpi_service=rpi_service,
    )

    service.close()

    assert service.thermo_control_thread_is_running is False
    assert rpi_service.closed is True
