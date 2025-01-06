# ruff: noqa: D100,D103,I001,S101,PLR2004
import snake
import pygame

def test_fruit_creation() -> None:
    red = pygame.Color("red")
    tile = snake.Tile(1, 2, red)
    fruit = snake.Fruit(tile)
    assert list(fruit.tiles) == [tile]
    assert next(fruit.tiles).color == red

def test_fruit_random_creation() -> None:
    for n_lines in range(1,3):
        for n_cols in range(1,4):
            fruit = snake.Fruit.create_random(nb_lines = n_lines,
                                              nb_cols = n_cols)
            assert len(list(fruit.tiles)) == 1
            tile = next(fruit.tiles)
            assert 0 <= tile.x < n_cols
            assert 0 <= tile.y < n_lines
