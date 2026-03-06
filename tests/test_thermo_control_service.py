import logging

from thermocontrol.application.services.thermo_control_service import ThermoControlService
from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.rpi_service_interface import RpiServiceInterface
from thermocontrol.domain.services.temperature_service_interface import TemperatureServiceInterface
from thermocontrol.shared.constants import LogMessages


class FakeTemperatureService(TemperatureServiceInterface):
    def __init__(self, temperatures: list[float | None]):
        self.temperatures = temperatures

    def get_temperature_ai_module(self) -> float | None:
        return self.temperatures.pop(0)


class FakeRpiService(RpiServiceInterface):
    def __init__(self):
        self.toggles = []
        self.closed = False

    def toggle_ai_cooler(self, enable: bool) -> None:
        self.toggles.append(enable)

    def close(self) -> None:
        self.closed = True


def test_control_ai_module_fan_once_turns_on_fan_at_or_above_threshold(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([55.0]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [True]
    assert LogMessages.FAN_ENABLED_AT_TEMP % 55.0 in caplog.text


def test_control_ai_module_fan_once_turns_off_fan_below_threshold(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([60.0, 54.9]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [True, False]
    assert LogMessages.FAN_ENABLED_AT_TEMP % 60.0 in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP % 54.9 in caplog.text


def test_control_ai_module_fan_once_does_not_log_without_state_transition(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([56.0, 57.0]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [True, True]
    assert caplog.text.count(LogMessages.FAN_ENABLED_AT_TEMP.split("%s")[0]) == 1
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text


def test_control_ai_module_fan_once_keeps_fan_off_when_temperature_unavailable(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=0)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([None]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False]
    assert LogMessages.FAN_ENABLED_AT_TEMP.split("%s")[0] not in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text


def test_close_stops_loop_and_closes_rpi_service() -> None:
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=ContextEntity(),
        temperature_service=FakeTemperatureService([0.0]),
        rpi_service=rpi_service,
    )

    service.close()

    assert service.thermo_control_thread_is_running is False
    assert rpi_service.closed is True
