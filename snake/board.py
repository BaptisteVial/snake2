# ruff: noqa: D100,S311

# Standard
import typing

# Third party
import pygame

# First party
from .fruit import Fruit
from .game_object import GameObject
from .observer import Observer
from .subject import Subject


class Board(Subject, Observer):
    """Main class that handles all game objects."""

    def __init__(self, screen: pygame.Surface, nb_lines: int, nb_cols: int,
                 tile_size: int) -> None:
        """Object initialization."""
        super().__init__()
        self._screen = screen
        self._nb_lines = nb_lines
        self._nb_cols = nb_cols
        self._tile_size = tile_size
        self._objects: list[GameObject] = []

    def add_object(self, obj: GameObject) -> None:
        """Add an object to the board."""
        # Add object if not already there
        if obj not in self._objects:
            self._objects.append(obj)
            obj.attach_obs(self)

    def remove_object(self, obj: GameObject) -> None:
        """Remove an object from the board."""
        # Add object if not already there
        if obj in self._objects:
            self._objects.remove(obj)
            obj.detach_obs(self)

    def create_fruit(self) -> None:
        """Create a random fruit."""
        fruit = None
        while fruit is None or list(self.collides(fruit)):
            fruit = Fruit.create_random(self._nb_lines, self._nb_cols)
        self.add_object(fruit)

    def draw(self) -> None:
        """Draw all objects on screen."""
        # Loop on all objects
        for obj in self._objects:

            # Loop on all object's tiles
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def notify_object_eaten(self, obj: GameObject) -> None:
        """Notify that the fruit has been eaten."""
        if isinstance(obj, Fruit):
            # Remove the fruit
            self.remove_object(obj)

            # Create a new fruit
            self.create_fruit()

    def notify_object_moved(self, obj: GameObject) -> None:
        """Notify that an object has moved."""
        # Detect board exit
        for tile in obj.tiles:
            if not (0 <= tile.x < self._nb_cols and
                    0 <= tile.y < self._nb_lines):
                obj.notify_out_of_board(width = self._nb_cols,
                                        height = self._nb_lines)

        # Detect collisions
        for o in self.collides(obj):
            obj.notify_collision(o)

    def collides(self, obj: GameObject) -> typing.Iterator[GameObject]:
        """Check if an object collides with other objects on the board."""
        # Loop on all known objects
        for o in self._objects:

            # Detect a collision
            if obj != o and not o.is_background() and obj in o:
                yield o
