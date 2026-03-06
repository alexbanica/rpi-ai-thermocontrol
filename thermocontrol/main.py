"""Main runtime module."""

from thermocontrol.presentation.controllers.runtime_controller import RuntimeController


def main() -> int:
    return RuntimeController().run()
