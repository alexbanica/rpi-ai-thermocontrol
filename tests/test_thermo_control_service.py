import logging
from typing import Optional

from thermocontrol.application.services.thermo_control_service import ThermoControlService
from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.domain.services.rpi_service_interface import RpiServiceInterface
from thermocontrol.domain.services.temperature_service_interface import TemperatureServiceInterface
from thermocontrol.shared.constants import LogMessages


class FakeTemperatureService(TemperatureServiceInterface):
    def __init__(self, temperatures: list[Optional[float]]):
        self.temperatures = temperatures

    def get_temperature_ai_module(self) -> Optional[float]:
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
    context = ContextEntity(ai_temperature_threshold=55, ai_temperature_average_read_count=1)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([55.0]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [True]
    assert LogMessages.FAN_ENABLED_AT_TEMP % (55.0, 55) in caplog.text


def test_control_ai_module_fan_once_turns_off_fan_below_threshold(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55, ai_temperature_average_read_count=1)
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
    assert LogMessages.FAN_ENABLED_AT_TEMP % (60.0, 55) in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP % (54.9, 55) in caplog.text


def test_control_ai_module_fan_once_does_not_log_without_state_transition(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55, ai_temperature_average_read_count=1)
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
    context = ContextEntity(ai_temperature_threshold=0, ai_temperature_average_read_count=1)
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


def test_control_ai_module_fan_once_waits_for_full_window_before_first_decision(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55, ai_temperature_average_read_count=3)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([60.0, 60.0, 60.0]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False, False]
    assert LogMessages.FAN_ENABLED_AT_TEMP.split("%s")[0] not in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False, False, True]
    assert LogMessages.FAN_ENABLED_AT_TEMP % (60.0, 55) in caplog.text


def test_control_ai_module_fan_once_uses_default_five_read_warm_up(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=55)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([60.0] * 5),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        for _ in range(4):
            service.control_ai_module_fan_once()

    assert context.ai_temperature_average_read_count == 5
    assert rpi_service.toggles == [False, False, False, False]
    assert service.is_fan_enabled is False
    assert LogMessages.FAN_ENABLED_AT_TEMP.split("%s")[0] not in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False, False, False, False, True]
    assert service.is_fan_enabled is True
    assert LogMessages.FAN_ENABLED_AT_TEMP % (60.0, 55) in caplog.text


def test_control_ai_module_fan_once_uses_sliding_average_and_evicts_oldest_reading() -> None:
    context = ContextEntity(ai_temperature_threshold=50, ai_temperature_average_read_count=2)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([49.0, 53.0, 47.0, 46.0]),
        rpi_service=rpi_service,
    )

    for _ in range(4):
        service.control_ai_module_fan_once()

    # Warm-up, above threshold (51), equality (50), then below threshold (46.5).
    assert rpi_service.toggles == [False, True, True, False]


def test_control_ai_module_fan_once_retains_window_across_unavailable_read(caplog) -> None:
    context = ContextEntity(ai_temperature_threshold=50, ai_temperature_average_read_count=3)
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService([60.0, 60.0, 60.0, None, 60.0]),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        for _ in range(4):
            service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False, False, True, False]
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()

    # The unavailable read forces off. Recovery immediately decides from the
    # retained full window; it does not begin another warm-up period.
    assert rpi_service.toggles == [False, False, True, False, True]


def test_control_ai_module_fan_once_logs_unrounded_decision_average_only_on_transitions(
    caplog,
) -> None:
    threshold = 55.15
    temperatures = [55.1, 55.2, 55.3, 54.0]
    enabled_average = sum(temperatures[:3]) / 3
    disabled_average = sum(temperatures[1:]) / 3
    context = ContextEntity(
        ai_temperature_threshold=threshold,
        ai_temperature_average_read_count=3,
    )
    rpi_service = FakeRpiService()
    service = ThermoControlService(
        context=context,
        temperature_service=FakeTemperatureService(temperatures),
        rpi_service=rpi_service,
    )

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()
        service.control_ai_module_fan_once()

    assert LogMessages.FAN_ENABLED_AT_TEMP.split("%s")[0] not in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP.split("%s")[0] not in caplog.text

    with caplog.at_level(logging.INFO):
        service.control_ai_module_fan_once()
        service.control_ai_module_fan_once()

    assert rpi_service.toggles == [False, False, True, False]
    assert LogMessages.FAN_ENABLED_AT_TEMP % (enabled_average, threshold) in caplog.text
    assert LogMessages.FAN_DISABLED_AT_TEMP % (disabled_average, threshold) in caplog.text


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
