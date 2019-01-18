import pygame
import os


class Path(pygame.sprite.Sprite):
    def __init__(self, dimensions, position, indexes, all_tiles):
        pygame.sprite.Sprite.__init__(self)

        assets_folder = os.path.join(os.path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(os.path.join(assets_folder, self.determine_image(indexes, all_tiles))).convert()

        # Rescale the image
        self.image = pygame.transform.scale(self.image, list(map(int, dimensions)))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0] + dimensions[0] / 2, position[1] + dimensions[1] / 2)

    def determine_image(self, indexes, all_tiles):
        east = False
        # If a tile exists to the right (east) of the current position
        if len(all_tiles[indexes[0]]) > indexes[1]:
            east = all_tiles[indexes[0]][indexes[1] + 1] == "d"

        west = False
        # If a tile exists on the left (west) of current position
        if indexes[1] - 1 > 0:
            west = all_tiles[indexes[0]][indexes[1] - 1] == "d"

        south = False
        # If a tile exists to the bottom (south) of the current position
        if len(all_tiles) > indexes[0]:
            south = all_tiles[indexes[0] + 1][indexes[1]] == "d"

        north = False
        # If a tile exists on the top (north) of current position
        if indexes[0] - 1 > 0:
            north = all_tiles[indexes[0] - 1][indexes[1]] == "d"

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
            return 'tileGrass_roadCrossing.png'
