from pathlib import Path

import pytest

from thermocontrol.domain.entities.context_entity import ContextEntity
from thermocontrol.infrastructure.parsers.yaml_config_parser import YamlConfigParser


def test_yaml_config_parser_applies_config_values(tmp_path: Path) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        """
thermocontrol:
  check_interval: 12
  ai_module:
    temperature_threshold: 58
    temperature_average_read_count: 3
    thermo_control_gpio_pin: 22
    thermo_control_hwmon: hwmon3,hwmon4
""".strip()
    )

    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    parser.parse_config(context, ["config.yml"])

    assert context.thermo_check_interval == 12
    assert context.ai_temperature_threshold == 58
    assert context.ai_temperature_average_read_count == 3
    assert context.ai_thermo_control_gpio_pin == 22
    assert context.ai_thermo_control_hwmon == "hwmon3,hwmon4"


def test_yaml_config_parser_keeps_defaults_when_missing(tmp_path: Path) -> None:
    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    parser.parse_config(context, ["does-not-exist.yml"])

    assert context.thermo_check_interval == 5
    assert context.ai_temperature_threshold == 20
    assert context.ai_temperature_average_read_count == 5
    assert context.ai_thermo_control_gpio_pin == 18
    assert context.ai_thermo_control_hwmon == "hwmon1"


def test_yaml_config_parser_defaults_average_read_count_when_key_absent(
    tmp_path: Path,
) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        """
thermocontrol:
  ai_module:
    temperature_threshold: 58
""".strip()
    )
    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    parser.parse_config(context, ["config.yml"])

    assert context.ai_temperature_average_read_count == 5


@pytest.mark.parametrize(
    "invalid_value",
    ["true", "false", "0", "-1", "2.5", '"3"', "null"],
    ids=["true", "false", "zero", "negative", "float", "string", "null"],
)
def test_yaml_config_parser_rejects_invalid_temperature_average_read_count(
    tmp_path: Path, invalid_value: str
) -> None:
    config_file = tmp_path / "config.yml"
    config_file.write_text(
        f"""
thermocontrol:
  ai_module:
    temperature_average_read_count: {invalid_value}
""".strip()
    )
    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    with pytest.raises(ValueError):
        parser.parse_config(context, ["config.yml"])
