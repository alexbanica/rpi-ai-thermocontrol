"""Temperature access boundary for infrastructure implementations."""

from abc import ABC, abstractmethod
from typing import Optional


class TemperatureServiceInterface(ABC):
    @abstractmethod
    def get_temperature_ai_module(self) -> Optional[float]:
        """Read AI module temperature in Celsius, or None when unavailable."""
