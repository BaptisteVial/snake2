# ruff: noqa: D100,S311

# Standard
import typing

# Third party
import pygame

# First party
from .game_object import GameObject
from .tile import Tile

# Colors
CB_COLOR_1 = pygame.Color("White")
CB_COLOR_2 = pygame.Color("Black")

class Checkerboard(GameObject):
    """The black and white checkerboard used as background."""

    def __init__(self, nb_lines: int, nb_cols: int) -> None:
        """Object initialization."""
        super().__init__()
        self._nb_lines = nb_lines
        self._nb_cols = nb_cols

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        """Tiles generator."""
        # Loop on all tiles
        for i in range(self._nb_cols):
            for j in range(self._nb_lines):

                # Generate the tile with the right color
                yield Tile(i, j, CB_COLOR_1 if (i+j) % 2 == 0 else CB_COLOR_2)

    def is_background(self) -> bool:
        """Test if this object is a background object."""
        return True
