"""GPIO fan control boundary for infrastructure implementations."""

from abc import ABC, abstractmethod


class RpiServiceInterface(ABC):
    @abstractmethod
    def toggle_ai_cooler(self, enable: bool) -> None:
        """Enable or disable the AI module fan."""

    @abstractmethod
    def close(self) -> None:
        """Release GPIO resources safely."""
