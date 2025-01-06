# ruff: noqa: D100,D103,I001,S101,PLR2004
import snake
import pygame

def test_tile_creation() -> None:
    black = pygame.Color("black")
    assert snake.Tile(1, 2, black).x == 1
    assert snake.Tile(1, 2, black).y == 2
    assert snake.Tile(1, 2, black).color == black

def test_tile_eq() -> None:
    black = pygame.Color("black")
    white = pygame.Color("white")
    assert snake.Tile(1, 2, black) == snake.Tile(1, 2, white)
    assert snake.Tile(1, 2, black) != snake.Tile(1, 1, black)
    assert snake.Tile(1, 1, white) != snake.Tile(1, 2, white)

def test_tile_add() -> None:
    black = pygame.Color("black")
    white = pygame.Color("white")
    t1 = snake.Tile(1, 2, black)
    t2 = snake.Tile(3, 4, white)
    assert t1 + t2 == snake.Tile(4, 6, black)
    assert t2 + t1 == t1 + t2
    assert (t1 + t2).color == t1.color
    assert (t2 + t1).color == t2.color
    assert (t1 + snake.Dir.UP) == snake.Tile(1, 1, black)
    assert (t1 + snake.Dir.DOWN) == snake.Tile(1, 3, black)
    assert (t1 + snake.Dir.LEFT) == snake.Tile(0, 2, black)
    assert (t1 + snake.Dir.RIGHT) == snake.Tile(2, 2, black)

def test_tile_sub() -> None:
    black = pygame.Color("black")
    white = pygame.Color("white")
    t1 = snake.Tile(1, 2, black)
    t2 = snake.Tile(3, 4, white)
    assert t1 - t2 == snake.Tile(-2, -2, black)
    assert t2 - t1 ==  snake.Tile(2, 2, black)
    assert (t1 - t2).color == t1.color
    assert (t2 - t1).color == t2.color
    assert (t1 - snake.Dir.UP) == snake.Tile(1, 3, black)
    assert (t1 - snake.Dir.DOWN) == snake.Tile(1, 1, black)
    assert (t1 - snake.Dir.LEFT) == snake.Tile(2, 2, black)
    assert (t1 - snake.Dir.RIGHT) == snake.Tile(0, 2, black)
