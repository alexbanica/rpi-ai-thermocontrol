from pathlib import Path

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
    thermo_control_gpio_pin: 22
    thermo_control_hwmon: hwmon3,hwmon4
""".strip()
    )

    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    parser.parse_config(context, ["config.yml"])

    assert context.thermo_check_interval == 12
    assert context.ai_temperature_threshold == 58
    assert context.ai_thermo_control_gpio_pin == 22
    assert context.ai_thermo_control_hwmon == "hwmon3,hwmon4"


def test_yaml_config_parser_keeps_defaults_when_missing(tmp_path: Path) -> None:
    context = ContextEntity()
    parser = YamlConfigParser(str(tmp_path))

    parser.parse_config(context, ["does-not-exist.yml"])

    assert context.thermo_check_interval == 5
    assert context.ai_temperature_threshold == 20
    assert context.ai_thermo_control_gpio_pin == 18
    assert context.ai_thermo_control_hwmon == "hwmon1"
