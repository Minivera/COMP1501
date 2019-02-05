import pygame
import os

animation_lag = 10


class Emote(pygame.sprite.Sprite):
    emote_size = 16

    animation_length = 3

    emote_positions = {
        "circle": (0, 0),
        "cross": (0, 3),
        "music": (0, 6),
        "puzzled": (0, 9),
        "thumbs_up": (2, 0),
        "thumbs_down": (2, 3),
        "oops": (2, 6),
        "idea": (2, 9),
        "arrow_down": (4, 0),
        "arrow_up": (4, 3),
        "sleep": (4, 6),
        "poison": (4, 9),
        "heart": (6, 0),
        "heart_broken": (6, 3),
        "mist": (6, 6),
        "angry": (6, 9),
        "surprise": (8, 0),
        "question": (8, 3),
        "shield": (8, 6),
        "heat": (8, 9),
        "surprise_extra": (10, 0),
        "slow": (10, 3),
        "light": (10, 6),
        "moon": (10, 9),
    }

    def __init__(self, emote_type, scale, position):
        pygame.sprite.Sprite.__init__(self)
        self.emote_type = emote_type
        self.frame = 0
        self.scale = scale
        self.position = position
        self.initial_position = position
        self.image = ""
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = self.get_emote_image()

        # Rescale the image
        self.rect = self.image.get_rect()
        self.image = pygame.transform.scale(self.image, (self.rect[2] * self.scale, self.rect[3] * self.scale))

        # Set the image's rectangle
        trans_color = self.image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def get_emote_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/emotes/bubble_emotes.png')
        sheet = pygame.image.load(assets_folder).convert()

        if not self.emote_type or self.emote_type not in self.emote_positions:
            return pygame.Surface((1, 1))

        top = self.emote_positions[self.emote_type][0] * self.emote_size
        left = self.emote_positions[self.emote_type][1] * self.emote_size +\
            (self.frame // animation_lag) * self.emote_size
        return sheet.subsurface(pygame.Rect(left, top, self.emote_size, self.emote_size))

    def change_type(self, new_type):
        self.emote_type = new_type
        self.set_image()

    def animate(self):
        self.frame = self.frame + 1 if self.frame + 1 < self.animation_length * animation_lag else 0
        self.set_image()
