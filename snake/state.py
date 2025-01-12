# Standard
import enum

class State(enum.Enum):
    QUIT = 0
    PLAY = 1
    GAME_OVER = 2
    SCORES = 3
    INPUT_NAME = 4