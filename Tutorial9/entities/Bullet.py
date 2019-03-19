import pygame
import os
import math
from constants.Colours import colours


class Bullet(pygame.sprite.Sprite):
    speed = 5

    size = 10

    def __init__(self, target, position, damage, effect=None):
        pygame.sprite.Sprite.__init__(self)
        self.target = target
        self.position = position
        self.damage = damage
        self.effect = effect
        self.velocity = (0, 0)
        self.image = None
        self.exists = True
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface((self.size, self.size))
        assets_folder = os.path.join('assets', 'sprites')

        # get and resize the image
        bullet = pygame.image.load(os.path.join(assets_folder, 'bulletSand1.png')).convert_alpha()
        bullet = pygame.transform.scale(bullet, (self.size, self.size))

        self.image.blit(bullet, (0, 0))

        # rotate the tank according ot its direct
        bullet_angle = math.atan2(self.velocity[1], self.velocity[0])
        self.image = pygame.transform.rotate(self.image, math.degrees(bullet_angle))

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        trans_color = self.image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        return

    def seek(self):
        target_pos = self.target.position
        # If not, move the ball towards the current position of the target
        steps_number = max(abs(target_pos[0] - self.position[0]), abs(target_pos[1] - self.position[1]))

        dx = float(target_pos[0] - self.position[0]) / steps_number
        dy = float(target_pos[1] - self.position[1]) / steps_number
        self.velocity = (dx * self.speed, dy * self.speed)
        return

    def has_hit(self):
        return self.image.get_rect(center=self.position)\
            .colliderect(self.target.image.get_rect(center=self.target.position))

    def update(self):
        if not self.exists:
            return

        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )
        self.set_image()
