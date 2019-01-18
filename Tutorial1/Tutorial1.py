import pygame
import csv
from path import Path
from terrain import Terrain
from enemy import Enemy

width = 800
height = 600
frame_rate = 40


def main():
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()

    running = True

    tiles = find_map_size()
    pre_render(screen, tiles, all_sprites)

    while running:
        render(screen, tiles, all_sprites)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(frame_rate)


def read_csv(file_name):
    file = open(file_name, "r")
    return list(csv.reader(file))


def pre_render(screen, tiles, sprites):
    sprites.update()

    draw_map(tiles, sprites)

    sprites.draw(screen)
    pygame.display.update()


def render(screen, tiles, sprites):
    sprites.update()

    draw_enemies(screen, tiles, sprites)

    sprites.draw(screen)
    pygame.display.update()


def find_map_size():
    world_map = read_csv("map.csv")
    return [len(world_map), len(world_map[0])]


def draw_map(tiles, sprites):
    tiles_x = tiles[1]
    tiles_y = tiles[0]

    world_map = read_csv("map.csv")
    y = 0
    i = 0
    for row in world_map:
        x = 0
        j = 0
        tile_height = height / tiles_y
        for column in row:
            tile_width = width / tiles_x
            if column == "g":
                terrain_obj = Terrain((tile_width, tile_height), (x, y))
                sprites.add(terrain_obj)
            if column == "d":
                path_obj = Path((tile_width, tile_height), (x, y), (i, j), world_map)
                sprites.add(path_obj)
            x += tile_width
            j += 1
        y += tile_height
        i += 1


def draw_enemies(surface, tiles, sprites):
    tiles_x = tiles[1]
    tiles_y = tiles[0]

    entities = read_csv("entities.csv")
    skip = True
    for row in entities:
        if skip:
            skip = False
            continue

        tile_width = width / tiles_x
        tile_height = height / tiles_y
        enemy_obj = Enemy((tile_width, tile_height), (int(row[3]) * tile_width, int(row[4]) * tile_height))
        sprites.add(enemy_obj)


if __name__ == "__main__":
    main()
