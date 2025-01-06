# ruff: noqa: D100,S311

# Standard
import random
import typing

# Third party
import pygame

# First party
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .game_object import GameObject
from .tile import Tile

# Constants
DEF_HEAD_COLOR = pygame.Color("green")
DEF_BODY_COLOR = pygame.Color("darkgreen")

class Snake(GameObject):
    """The snake."""

    def __init__(self, tiles: list[Tile], direction: Dir, *,
                 gameover_on_exit: bool = False) -> None:
        """Object initialization."""
        super().__init__()
        self._tiles = tiles
        self._dir = direction
        self._length = len(tiles)
        self._gameover_on_exit = gameover_on_exit

    @property
    def length(self) -> int:
        """Snake length."""
        return self._length

    @property
    def tiles(self) -> typing.Iterator[Tile]:
        """Iterator on the tiles."""
        return iter(self._tiles)

    @property
    def dir(self) -> Dir:
        """Snake direction."""
        return self._dir

    @dir.setter
    def dir(self, direction: Dir) -> None:
        self._dir = direction

    def notify_out_of_board(self, width: int, height: int) -> None:
        """Snake has exited the board."""
        if self._gameover_on_exit:
            raise GameOver

        # Only the head has exited
        self._tiles[0].x = self._tiles[0].x % width
        self._tiles[0].y = self._tiles[0].y % height

    def notify_collision(self, obj: GameObject) -> None:
        """Notify that an object collides with another."""
        if isinstance(obj, Fruit):

            # Grow
            self._length += 1

            # Notify that the fruit has been eaten
            for obs in self.observers:
                obs.notify_object_eaten(obj)

    def move(self) -> None:
        """Let the snake advance."""
        # Create new head
        new_head = self._tiles[0] + self._dir

        # Slither on itself?
        if new_head in self._tiles:
            raise GameOver

        # Current head changes color
        self._tiles[0].color = self._tiles[-1].color

        # Insert new head
        self._tiles.insert(0, new_head)

        # Notify movement
        for obs in self.observers:
            obs.notify_object_moved(self)

        # Remove queue tiles if needed
        if len(self._tiles) > self._length:
            del self._tiles[self._length:]

    # Create a Snake at random position on the board
    @classmethod
    def create_random(cls, nb_lines: int, nb_cols: int, # noqa: PLR0913
                      length: int,
                      *,
                      head_color: pygame.Color = DEF_HEAD_COLOR,
                      body_color: pygame.Color = DEF_BODY_COLOR,
                      gameover_on_exit: bool = False) -> typing.Self:
        """Create a snake and place it randomly on the board."""
        tiles = [] # List of tuples (col_index, line_index)

        # Choose head
        random.seed()
        x = random.randint(length - 1, nb_cols - length)
        y = random.randint(length - 1, nb_lines - length)
        tiles.append(Tile(x, y, head_color))

        # Choose body orientation (i.e.: in which direction the snake will move)
        random.seed()
        snake_dir = random.sample([Dir.LEFT, Dir.RIGHT, Dir.UP, Dir.DOWN], 1)[0]

        # Create body
        while len(tiles) < length:
            tile = tiles[-1] - snake_dir
            tile.color = body_color
            tiles.append(tile)

        return cls(tiles, direction = snake_dir,
                   gameover_on_exit = gameover_on_exit)

