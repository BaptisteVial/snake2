# ruff: noqa: D100,S311

# Third party
import importlib.resources
import time

import pygame

# First party
from .board import Board
from .checkerboard import Checkerboard
from .dir import Dir
from .exceptions import GameOver
from .fruit import Fruit
from .snake import Snake
from .state import State
from .scores import Scores
from .score import Score

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
        self._snake = None
        self._current_score = 0
        self._state = None

    def _reset_snake(self) -> None:
        if self._snake is not None:
            self._board.detach_obs(self._snake)
            self._board.remove_object(self._snake)
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

    def _update_score(self) -> None:
        if self._state == State.PLAY:
            self._current_score = max(self._current_score, self._snake.length)
        if self._state == State.SCORES:
            self._current_score = 0


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
        self._reset_snake()
        self._update_score()

        # Initialisation des scores
        Scores.initialize_scores_file("snake_scores.yml")  # Fichier YAML pour les scores
        self._scores = Scores.default(5)
        self._scores.load_from_file("snake_scores.yml")

        # Create fruit
        Fruit.color = self._fruit_color
        self._board.create_fruit()

        #Upload fonts
        with importlib.resources.path("snake", "DejaVuSansMono-Bold.ttf") as f:
            self._fontscore = pygame.font.Font(f, 32)
            self._fontgameover = pygame.font.Font(f, 64)

    def _drawgameover(self) -> None:
        text_gameover = self._fontgameover.render("Game Over", True, pygame.Color("red"))  # noqa: E501, FBT003
        x, y = 80, 160
        self._screen.blit(text_gameover, (x, y))

    def _draw_scores(self) -> None:
        #mettre une ligne high scores
        x, y = 80, 10
        for score in self._scores:
            text_score = self._fontscore.render(score.name.ljust(Score.MAX_LENGTH)+ f"{score.score:.>8}", True, pygame.Color("red"))
            self._screen.blit(text_score, (x, y))
            y += 32


    def _process_scores_event(self, event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self._state = State.PLAY

    def _process_play_event(self, event) -> None:
        # Key press
        if event.type == pygame.KEYDOWN:
            # Quit
            match event.key:
                case pygame.K_UP:
                    self._snake.dir = Dir.UP
                case pygame.K_DOWN:
                    self._snake.dir = Dir.DOWN
                case pygame.K_LEFT:
                    self._snake.dir = Dir.LEFT
                case pygame.K_RIGHT:
                    self._snake.dir = Dir.RIGHT
        self._update_score()

    def _process_events(self) -> None:
        """Process pygame events."""
        # Loop on all events
        for event in pygame.event.get():

            match self._state:
                case State.SCORES:
                    self._process_scores_event(event)
                case State.PLAY:
                    self._process_play_event(event)
                case State.INPUT_NAME:
                    if self._process_input_name_event(event, input):
                        # L'utilisateur a validé son nom
                        name = "".join(input).strip()
                        self._scores.add_score(Score(name=name, score=self._current_score))
                        self._scores.save_to_file(args.scores_file)
                        self._state = State.SCORES


            # Closing window (Mouse click on cross icon or OS keyboard shortcut)
            if event.type == pygame.QUIT:
                self._state = State.QUIT

            if event.type == pygame.KEYDOWN:
                match event.key:
                    case pygame.K_q:
                        self._state = State.QUIT
    
    def _process_input_name_event(self, event, input: list[str]) -> bool:
        """Gère les événements lors de la saisie du nom."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:  # L'utilisateur valide le nom
                return True
            elif event.key == pygame.K_BACKSPACE:  # Supprimer le dernier caractère
                if input:
                    input.pop()
            else:  # Ajouter un caractère s'il est imprimable
                char = event.unicode
                if len(input) < Score.MAX_LENGTH and char.isprintable():
                    input.append(char)
        return False

    def _draw_input_name(self, input: list[str]) -> None:
        """Affiche l'écran de saisie du nom."""
        self._screen.fill((0, 0, 0))  # Fond noir
        prompt_text = self._fontscore.render("Enter your name:", True, pygame.Color("white"))
        name_text = self._fontscore.render("".join(input), True, pygame.Color("green"))
        self._screen.blit(prompt_text, (80, 160))
        self._screen.blit(name_text, (80, 200))
        pygame.display.update()

    def start(self) -> None:
        """Start the game."""
        # Initialize pygame
        pygame.init()

        # Initialize game
        self._init()

        # Start pygame loop
        self._state = State.SCORES
        while self._state != State.QUIT:

            # Wait 1/FPS second
            self._clock.tick(self._fps)

            # Listen for events
            self._process_events()

            # Update objects
            self._update_score()
            try:
                if self._state == State.PLAY:
                    self._snake.move()
            except GameOver:
                self._state = State.GAME_OVER
                self._update_score()
                cpt = self._fps

            # Draw
            self._board.draw()
            match self._state:
                case State.GAME_OVER:
                    self._drawgameover()
                    cpt -= 1
                    if cpt == 0:
                        score = self._current_score
                        self._reset_snake()
                        if self._scores.is_high_score(score):
                            print("New high score!")
                            self._state = State.INPUT_NAME
                        else:
                            self._state = State.SCORES
                case State.INPUT_NAME:
                    self._draw_input_name(input_buffer)
                case State.SCORES:
                    self._draw_scores()

            # Display
            pygame.display.set_caption(f"Current score is {self._current_score}")
            pygame.display.update()

        # Terminate pygame
        pygame.quit()