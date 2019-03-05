import pygame
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

        # Render the map squares
        i = 0
        for row in self.map:
            j = 0
            for column in row:
                tile = pygame.Surface(self.square_size)
                if column["type"] == types["path"]:
                    tile.fill(colours["paths"])
                elif column["type"] == types["grass"]:
                    tile.fill(colours["grass"])
                #elif column["type"] == types["souvenir_shop"]:

                #elif column["type"] == types["flower_shop"]:

                #elif column["type"] == types["clothes_shop"]:

                #elif column["type"] == types["food_shop"]:

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
