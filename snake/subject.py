# ruff: noqa: D100,S311

# First party
from .observer import Observer


class Subject:
    """Mother class representing a subject for the Observer pattern."""

    def __init__(self) -> None:
        """Object initialization."""
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        """List of observers."""
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        """Attach an observer."""
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        """Detach an observer."""
        self._observers.remove(obs)
