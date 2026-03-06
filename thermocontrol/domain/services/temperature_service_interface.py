"""Temperature access boundary for infrastructure implementations."""

from abc import ABC, abstractmethod


class TemperatureServiceInterface(ABC):
    @abstractmethod
    def get_temperature_ai_module(self) -> float:
        """Read AI module temperature in Celsius."""
