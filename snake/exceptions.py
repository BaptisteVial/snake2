# ruff: noqa: D100,S311

class SnakeException(Exception): # noqa: N818
    """Exception super-class for all Snake exceptions."""

    def __init__(self, msg: str) -> None:
        """Object initialization."""
        super().__init__(msg)

class GameOver(SnakeException):
    """Exception class used to signal game over."""

    def __init__(self) -> None:
        """Object initialization."""
        super().__init__("Game over!")

class SnakeError(Exception):
    """Exception super-class for all Snake errors."""

    def __init__(self, msg: str) -> None:
        """Object initialization."""
        super().__init__(msg)

class IntRangeError(SnakeError):
    """Exception for integer range error."""

    def __init__(self, label: str, value: int, low: int, high: int) -> None:
        """Object initialization."""
        super().__init__(f"{label} value must be between {low} and {high}."
                         f" {value} is not allowed.")

class ColorError(SnakeError):
    """Exception for color format error."""

    def __init__(self, color: str) -> None:
        """Object initialization."""
        super().__init__(f'Color "{color}" does not respect the HTML'
                         ' hexadecimal format #rrggbb.')

