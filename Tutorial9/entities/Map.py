import pygame
import math
import os
import random
from constants.Colours import colours
from constants.Types import types


class Map(pygame.sprite.Sprite):
    def __init__(self, dimensions, position, world_map):
        pygame.sprite.Sprite.__init__(self)
        self.dimensions = dimensions
        self.position = position
        self.map = world_map
        self.square_size = (
            dimensions[0] // len(world_map),
            dimensions[1] // len(world_map[0]),
        )
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface(self.dimensions)
        assets_folder = os.path.join('assets', 'sprites')
        grass1 = pygame.image.load(os.path.join(assets_folder, 'tileGrass1.png')).convert()
        grass2 = pygame.image.load(os.path.join(assets_folder, 'tileGrass2.png')).convert()

        # Render the map squares
        i = 0
        for row in self.map:
            j = 0
            for column in row:
                tile = pygame.Surface(self.square_size)
                if column["type"] == types["path"]:
                    path_image = pygame.image.load(os.path.join(
                        assets_folder,
                        self.determine_path_image((i, j)))
                    ).convert()
                    path_image = pygame.transform.scale(path_image, self.square_size)
                    tile.blit(path_image, (0, 0))
                elif column["type"] == types["grass"]:
                    grass_image = grass1 if random.randint(1, 2) == 1 else grass2
                    grass_image = pygame.transform.scale(grass_image, self.square_size)
                    tile.blit(grass_image, (0, 0))

                # draw a white border around each tile to show the grid
                pygame.draw.rect(
                    tile,
                    colours["border"],
                    (
                        0,
                        0,
                        self.square_size[0],
                        self.square_size[1]
                    ),
                    1)
                # Draw the tile on the map
                self.image.blit(
                    tile,
                    (
                        self.square_size[0] * j,
                        self.square_size[1] * i,
                    ),
                )
                j += 1
            i += 1

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )
        return

    def set_map(self, new_map):
        self.map = new_map
        self.square_size = (
            self.dimensions[0] // len(new_map),
            self.dimensions[1] // len(new_map[0]),
        )
        self.set_image()
        return

    def square_under_mouse(self, position):
        x = math.floor(position[0] / self.square_size[0])
        y = math.floor(position[1] / self.square_size[1])
        return self.map[y][x]

    def determine_path_image(self, pos):
        east = False
        # If a tile exists to the right (east) of the current position
        if len(self.map[pos[0]]) - 1 > pos[1]:
            east = self.map[pos[0]][pos[1] + 1]["type"] == types["path"]

        west = False
        # If a tile exists on the left (west) of current position
        if pos[1] - 1 > 0:
            west = self.map[pos[0]][pos[1] - 1]["type"] == types["path"]

        south = False
        # If a tile exists to the bottom (south) of the current position
        if len(self.map) - 1 > pos[0]:
            south = self.map[pos[0] + 1][pos[1]]["type"] == types["path"]

        north = False
        # If a tile exists on the top (north) of current position
        if pos[0] - 1 > 0:
            north = self.map[pos[0] - 1][pos[1]]["type"] == types["path"]

        if north & south & west & east:
            return 'tileGrass_roadCrossing.png'
        elif north & south & west:
            return 'tileGrass_roadSplitW.png'
        elif north & south & east:
            return 'tileGrass_roadSplitE.png'
        elif north & east & west:
            return 'tileGrass_roadSplitN.png'
        elif south & east & west:
            return 'tileGrass_roadSplitS.png'
        elif north & east:
            return 'tileGrass_roadCornerUR.png'
        elif north & west:
            return 'tileGrass_roadCornerUL.png'
        elif south & east:
            return 'tileGrass_roadCornerLR.png'
        elif south & west:
            return 'tileGrass_roadCornerLL.png'
        elif west & east:
            return 'tileGrass_roadEast.png'
        elif north & south:
            return 'tileGrass_roadNorth.png'
        else:
            return 'tileGrass_roadNorth.png'
