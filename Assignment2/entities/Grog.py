import os
import math
import pygame
from pygame import gfxdraw


class Grog(pygame.sprite.Sprite):
    black = (2, 2, 2)
    white = (255, 255, 255)

    def __init__(self, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.dimensions = dimensions
        self.mouse_pos = (0, 0)
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/large')
        self.image = pygame.Surface(self.dimensions)

        # Load the mouth image
        mouth = pygame.image.load(os.path.join(assets_folder, "MonsterGameAssets-019.png")).convert()
        mouth = pygame.transform.scale(mouth, self.dimensions)
        mouth_rect = mouth.get_rect()

        # Place it in the middle
        self.image.blit(mouth, mouth_rect)

        # Draw the eyes
        left_eye = pygame.Surface((50, 50))
        gfxdraw.filled_circle(
            left_eye,
            25,
            25,
            25,
            self.white
        )
        gfxdraw.aacircle(
            left_eye,
            25,
            25,
            25,
            self.white
        )
        gfxdraw.filled_circle(
            left_eye,
            25,
            40,
            5,
            self.black
        )
        gfxdraw.aacircle(
            left_eye,
            25,
            40,
            5,
            self.black
        )
        trans_color = left_eye.get_at((0, 0))
        left_eye.set_colorkey(trans_color)
        left_eye_pos = (
            (self.dimensions[0] / 2 - mouth_rect[2] / 2) + 10,
            25
        )

        right_eye = left_eye.copy()
        right_eye_pos = (
            (self.dimensions[0] / 2 + mouth_rect[2] / 2) - 60,
            25
        )
        trans_color = right_eye.get_at((0, 0))
        right_eye.set_colorkey(trans_color)

        # Rotate the eyes to place the cursor
        left_eye = pygame.transform.rotate(
            left_eye,
            -(math.atan2(
                left_eye_pos[1] - self.mouse_pos[1],
                left_eye_pos[0] - self.mouse_pos[0]
            )) * 180 / math.pi + 270
        )
        right_eye = pygame.transform.rotate(
            right_eye,
            -(math.atan2(
                right_eye_pos[1] - self.mouse_pos[1],
                right_eye_pos[0] - self.mouse_pos[0]
            )) * 180 / math.pi + 270
        )

        # Draw the two eyes
        self.image.blit(left_eye, left_eye_pos)
        self.image.blit(right_eye, right_eye_pos)

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )

    def change_mouse_pos(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.set_image()
