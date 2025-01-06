# ruff: noqa: D100,S311

# Standard
import abc
import typing

# First party
from .observer import Observer
from .subject import Subject
from .tile import Tile


class GameObject(Subject, Observer, abc.ABC):
    """Abstract class for all game objects."""

    def __init__(self) -> None:
        """Object initialization."""
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> typing.Iterator[Tile]:
        """The tiles of the object."""
        raise NotImplementedError

    def __contains__(self, other: object) -> bool:
        """Check if an game object intersects with another."""
        if not isinstance(other, GameObject):
            return False
        return any(t in self.tiles for t in other.tiles)

    def is_background(self) -> bool:
        """Tell if this object is a background object."""
        return False
