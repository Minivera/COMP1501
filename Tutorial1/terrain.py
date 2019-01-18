import pygame
import os
import random


class Terrain(pygame.sprite.Sprite):
    def __init__(self, dimensions, position):
        pygame.sprite.Sprite.__init__(self)

        assets_folder = os.path.join(os.path.dirname(__file__), 'Assets')
        self.image = pygame.image.load(os.path.join(assets_folder, self.determine_image())).convert()

        # Rescale the image
        self.image = pygame.transform.scale(self.image, list(map(int, dimensions)))
        self.rect = self.image.get_rect()
        self.rect.center = (position[0] + dimensions[0] / 2, position[1] + dimensions[1] / 2)

    def determine_image(self):
        images = ('tileGrass1.png', 'tileGrass2.png')

        return images[random.randint(0, 1)]
