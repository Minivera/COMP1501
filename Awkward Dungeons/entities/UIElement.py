import pygame
import os


class UIElement(pygame.sprite.Sprite):
    def __init__(self, scale, position, position_on_sheet):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.position_on_sheet = position_on_sheet
        self.initial_position = position
        self.scale = scale
        self.image = ""
        self.rect = ()
        self.set_image()

    def set_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/ui/ui_split.png')
        sheet = pygame.image.load(assets_folder)

        width = self.position_on_sheet[2] - self.position_on_sheet[0]
        height = self.position_on_sheet[3] - self.position_on_sheet[1]

        self.image = sheet.subsurface(pygame.Rect(self.position_on_sheet[0], self.position_on_sheet[1], width, height))

        # Rescale the image
        self.image = pygame.transform.scale(self.image, (width * self.scale, height * self.scale))

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect[2], self.rect[3])

    def reset_position(self):
        self.position = self.initial_position
