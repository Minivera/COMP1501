import pygame
import os

animation_lag = 10


class Animated(pygame.sprite.Sprite):
    def __init__(self, unit_type, state, animation_length, scale, position, orientation=0):
        pygame.sprite.Sprite.__init__(self)
        self.unit_type = unit_type
        self.state = state
        self.frame = 0
        self.anim_length = animation_length
        self.scale = scale
        self.position = position
        self.initial_position = position
        self.orientation = orientation
        self.image = ""
        self.rect = ()
        self.set_image()

    def set_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/units')
        self.image = pygame.image.load(os.path.join(assets_folder, self.determine_image())).convert()

        # Rescale the image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect[2] * self.scale, self.rect[3] * self.scale))

        # Rotate the image
        self.image = pygame.transform.flip(self.image, False if self.orientation == 0 else True, False)

        # Set the image's rectangle
        trans_color = self.image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def change_state(self, new_state):
        self.state = new_state
        self.set_image()

    def change_type(self, new_type):
        self.unit_type = new_type
        self.set_image()

    def animate(self):
        self.frame = self.frame + 1 if self.frame + 1 < self.anim_length * animation_lag else 0
        self.set_image()

    def rotate(self, orientation):
        self.orientation = orientation
        self.set_image()

    def reset_position(self):
        self.position = self.initial_position

    def determine_image(self):
        return "{}_{}_anim_f{}.png".format(self.unit_type, self.state, self.frame // animation_lag)
