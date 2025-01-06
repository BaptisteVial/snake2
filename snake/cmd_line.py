# ruff: noqa: D100,S311

# Standard
import argparse
import re

# Third party
import pygame

# First party
from .exceptions import ColorError, IntRangeError

# Global constants
DEFAULT_HEIGHT = 24 # Number of lines
DEFAULT_WIDTH = 32 # Number of columns
DEFAULT_TILE_SIZE = 20
DEFAULT_FPS = 10 # Number of frames per second
MIN_HEIGHT = 12
MAX_HEIGHT = 100
MIN_WIDTH = 24
MAX_WIDTH = 100
MIN_TILE_SIZE = 10
MAX_TILE_SIZE = 30
MIN_FPS = 10
MAX_FPS = 30

# Snake constants
SK_DEF_HEAD_COLOR = pygame.Color("Green2") # Snake's head default color
SK_DEF_BODY_COLOR = pygame.Color("GreenYellow") # Snake's body default color
SK_DEF_HEAD_COLOR_HEX = (f"#{SK_DEF_HEAD_COLOR.r:02x}{SK_DEF_HEAD_COLOR.g:02x}"
                     f"{SK_DEF_HEAD_COLOR.b:02x}")
SK_DEF_BODY_COLOR_HEX = (f"#{SK_DEF_BODY_COLOR.r:02x}{SK_DEF_BODY_COLOR.g:02x}"
                     f"{SK_DEF_BODY_COLOR.b:02x}")

# Fruit constants
FRUIT_DEF_COLOR = pygame.Color("Red3") # Fruit default color
FRUIT_DEF_COLOR_HEX = (f"#{FRUIT_DEF_COLOR.r:02x}{FRUIT_DEF_COLOR.g:02x}"
                       f"{FRUIT_DEF_COLOR.b:02x}")

def read_args() -> argparse.Namespace:
    """Read command line arguments."""
    # Create parser & set description
    parser = argparse.ArgumentParser(
            description = "Game of the Snake.",
            formatter_class = argparse.ArgumentDefaultsHelpFormatter)

    # Checkerboard arguments
    parser.add_argument("--tile-size", "-T", type = int,
                        default = DEFAULT_TILE_SIZE,
                        help=f"Tile size, in pixels. Must be between"
                        f" {MIN_TILE_SIZE} and {MAX_TILE_SIZE}.")
    parser.add_argument("--height", "-H", type = int, default = DEFAULT_HEIGHT,
                        help="Number of lines of the checkerboard."
                        f" Must be between {MIN_HEIGHT} and {MAX_HEIGHT}.")
    parser.add_argument("--width", "-W", type = int, default = DEFAULT_WIDTH,
                        help="Number of columns of the checkerboard."
                        f" Must be between {MIN_WIDTH} and {MAX_WIDTH}.")

    # Colors
    parser.add_argument("--fruit-color", default = FRUIT_DEF_COLOR_HEX,
                        help="Color of the fruit.")
    parser.add_argument("--snake-head-color", default = SK_DEF_HEAD_COLOR_HEX,
                        help="Color of the snake's head.")
    parser.add_argument("--snake-body-color", default = SK_DEF_BODY_COLOR_HEX,
                        help="Color of the snake's body.")

    # Game options
    parser.add_argument("--gameover-on-exit", action = "store_true",
                        help="Exiting the board ends the game.")

    # FPS
    parser.add_argument("--fps", type = int, default = DEFAULT_FPS,
                        help="Set the number of frames per second."
                        f" Must be between {MIN_FPS} and {MAX_FPS}.")

    # Parse
    args = parser.parse_args()

    # Check integer range
    for chk in [{"lbl": "Tile size", "val": args.tile_size,
                 "min": MIN_TILE_SIZE, "max": MAX_TILE_SIZE},
                {"lbl": "Width", "val": args.width,
                 "min": MIN_WIDTH, "max": MAX_WIDTH},
                {"lbl": "Height", "val": args.height,
                 "min": MIN_HEIGHT, "max": MAX_HEIGHT},
                {"lbl": "FPS", "val": args.fps,
                 "min": MIN_FPS, "max": MAX_FPS},
                ]:
        if not (chk["min"] <= chk["val"] <= chk["max"]):
            raise IntRangeError(chk["lbl"], chk["val"], chk["min"], chk["max"])

    # Check colors
    for color in [args.fruit_color, args.snake_head_color,
                  args.snake_body_color]:
        if not re.match(r"^#[0-9a-fA-F]{6}$", color):
            raise ColorError(color)

    # Run parser on command line arguments
    return args

