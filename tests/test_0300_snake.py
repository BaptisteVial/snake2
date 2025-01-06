# ruff: noqa: D100,D103,I001,S101,PLR2004
import snake
import pygame

def test_snake_creation() -> None:
    green = pygame.Color("green")
    snk = snake.Snake([snake.Tile(0,10,green), snake.Tile(0,11,green),
                       snake.Tile(0,12,green)], snake.Dir.UP)
    tiles = list(snk.tiles)
    assert snk.length == 3
    assert len(tiles) == 3
    assert tiles[0].x == 0
    assert tiles[0].y == 10
    assert tiles[0].color == green
    assert tiles[-1].color == green
    assert snk.dir == snake.Dir.UP

def test_snake_create_random() -> None:
    for n_lines in range(6,8):
        for n_cols in range(6,8):
            for length in range(3, 4):
                snk = snake.Snake.create_random(nb_lines = n_lines,
                                                nb_cols = n_cols,
                                                length = length)
                assert snk.length == length
                for tile in snk.tiles:
                    assert 0 <= tile.x < n_cols
                    assert 0 <= tile.y < n_lines

def test_snake_move() -> None:
    green = pygame.Color("green")
    snk = snake.Snake([snake.Tile(0,10,green), snake.Tile(0,11,green),
                       snake.Tile(0,12,green)], snake.Dir.UP)
    snk.move()
    tiles = list(snk.tiles)
    assert len(tiles) == 3
    assert tiles[0].x == 0
    assert tiles[0].y == 9
    assert tiles[1].y == 10
    assert tiles[2].y == 11

def test_in_op() -> None:
    green = pygame.Color("green")
    snk = snake.Snake([snake.Tile(0,10,green), snake.Tile(0,11,green),
                       snake.Tile(0,12,green)], snake.Dir.UP)
    assert snake.Fruit(snake.Tile(0,1,green)) not in snk
    assert snake.Fruit(snake.Tile(0,9,green)) not in snk
    assert snake.Fruit(snake.Tile(1,10,green)) not in snk
    assert snake.Fruit(snake.Tile(-1,10,green)) not in snk
    assert snake.Fruit(snake.Tile(0,10,green)) in snk
    assert snake.Fruit(snake.Tile(0,11,green)) in snk
    assert snake.Fruit(snake.Tile(0,12,green)) in snk
    assert snake.Fruit(snake.Tile(0,13,green)) not in snk
