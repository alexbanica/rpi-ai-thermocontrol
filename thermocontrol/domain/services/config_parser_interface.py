"""Configuration parsing boundary for infrastructure implementations."""

from abc import ABC, abstractmethod

from thermocontrol.domain.entities.context_entity import ContextEntity


class ConfigParserInterface(ABC):
    @abstractmethod
    def parse_config(self, context: ContextEntity, config_file_names: list[str]) -> None:
        """Parse available config files and mutate context values."""
