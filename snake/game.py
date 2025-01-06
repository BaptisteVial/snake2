# ruff: noqa: D100,S311

# Third party
import pygame

# First party
from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .snake import Snake

# Constants
SK_START_LENGTH = 3

class Game:
    """The main class of the game."""

    def __init__(self, width: int, height: int, tile_size: int, # noqa: PLR0913
                 fps: int,
                 *,
                 fruit_color: pygame.Color,
                 snake_head_color: pygame.Color,
                 snake_body_color: pygame.Color,
                 gameover_on_exit: bool,
                 ) -> None:
        """Object initialization."""
        self._width = width
        self._height = height
        self._tile_size = tile_size
        self._fps = fps
        self._fruit_color = fruit_color
        self._snake_head_color = snake_head_color
        self._snake_body_color = snake_body_color
        self._gameover_on_exit = gameover_on_exit

    def _init(self) -> None:
        """Initialize the game."""
        # Create a display screen
        screen_size = (self._width * self._tile_size,
                       self._height * self._tile_size)
        self._screen = pygame.display.set_mode(screen_size)

        # Create the clock
        self._clock = pygame.time.Clock()

        # Create the main board
        self._board = Board(screen = self._screen,
                            nb_lines = self._height,
                            nb_cols = self._width,
                            tile_size = self._tile_size)

        # Create checkerboard
        self._checkerboard = Checkerboard(nb_lines = self._height,
                                          nb_cols = self._width)
        self._board.add_object(self._checkerboard)

        # Create snake
        self._snake = Snake.create_random(
                nb_lines = self._height,
                nb_cols = self._width,
                length = SK_START_LENGTH,
                head_color = self._snake_head_color,
                body_color = self._snake_body_color,
                gameover_on_exit = self._gameover_on_exit,
                )
        self._board.add_object(self._snake)
        self._board.attach_obs(self._snake)

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()

    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():

            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._run = False

            # Key press
            if event.type == pygame.KEYDOWN:

                # Quit
                match event.key:
                    case pygame.K_q:
                        self._run = False
                    case pygame.K_UP:
                        self._snake.dir = Dir.UP
                    case pygame.K_DOWN:
                        self._snake.dir = Dir.DOWN
                    case pygame.K_LEFT:
                        self._snake.dir = Dir.LEFT
                    case pygame.K_RIGHT:
                        self._snake.dir = Dir.RIGHT

    def start(self) -> None:
        """Start the game."""
        # Initialize pygame
        pygame.init()

        try:
            # Initialize game
            self._init()

            # Start pygame loop
            self._run = True
            while self._run:

                # Wait 1/FPS second
                self._clock.tick(self._fps)

                # Listen for events
                self._process_events()

                # Update objects
                self._snake.move()

                # Draw
                self._board.draw()

                # Display
                pygame.display.update()

        except GameOver:
            print("Game over!") # noqa: T201

        # Terminate pygame
        pygame.quit()

