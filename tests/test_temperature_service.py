import logging
from io import StringIO

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.infrastructure.services.temperature_service import TemperatureService
from thermocontrol.shared.constants import LogMessages


def test_get_temperature_ai_module_returns_first_readable_hwmon(monkeypatch) -> None:
    context = ContextEntity(ai_thermo_control_hwmon="hwmon1,hwmon2")
    service = TemperatureService(context)

    def fake_open(path, mode="r", encoding="utf-8"):
        if "hwmon1" in path:
            raise FileNotFoundError("missing")
        if "hwmon2" in path:
            return StringIO("57000")
        raise AssertionError(f"unexpected path: {path}")

    monkeypatch.setattr("builtins.open", fake_open)

    assert service.get_temperature_ai_module() == 57.0


def test_get_temperature_ai_module_returns_none_when_all_hwmon_reads_fail(caplog, monkeypatch) -> None:
    context = ContextEntity(ai_thermo_control_hwmon="hwmon1,hwmon2")
    service = TemperatureService(context)

    def fake_open(path, mode="r", encoding="utf-8"):
        raise FileNotFoundError(f"missing path: {path}")

    monkeypatch.setattr("builtins.open", fake_open)

    with caplog.at_level(logging.WARNING):
        assert service.get_temperature_ai_module() is None

    assert LogMessages.TEMP_READ_FAILED.split("%s")[0] in caplog.text
    assert LogMessages.TEMP_READ_ALL_FAILED in caplog.text
