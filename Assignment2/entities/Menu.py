import os
import pygame
from entities.Colours import colours


class Menu(pygame.sprite.Sprite):
    title_font_size = 45
    font_size = 28

    title = "GROG!"
    instructions = [
        "Grog is hungry, feed him by changing the",
        "colours of the balls on the board",
        "according to his demands. Left-clicking",
        "on a ball will cycle through its possible",
        "colors. Right-clicking a ball will make",
        "all the other ball move towards the clicked",
        "ball. If a ball of the same color hits",
        "another ball, they will merge. If a ball",
        "of a different color hits another ball,",
        "they will reduce their value. Pressing 'r'",
        "will generate new balls. When Grog's demands",
        "are met, he will absorb all the balls and",
        "request a new meal. Score is calculated in",
        "clicks, with 'r' being worth 5 clicks. Try",
        "to feed grog in the least amount of clicks",
        "possible.",
        "",
        "Good luck!",
    ]

    def __init__(self, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.title_font = pygame.font.Font("assets/monogram_extended.ttf", self.title_font_size)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.position = position
        self.dimensions = dimensions
        self.button_rect = ()
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/large')
        self.image = pygame.Surface(self.dimensions)
        self.image.fill(colours["menu_bg"])

        # Draw the title in the center
        text = self.title_font.render(
            "Grog!",
            1,
            colours["white"]
        )
        text_rect = text.get_rect()
        self.image.blit(text, (
            self.dimensions[0] // 2 - text_rect[2] // 2,
            50,
        ))

        # Draw the instructions on the left
        pos = 150
        for instruction in self.instructions:
            text = self.main_font.render(
                instruction,
                1,
                colours["white"]
            )
            text_rect = text.get_rect()
            self.image.blit(text, (
                15,
                pos,
            ))
            pos += text_rect[3]

        # Draw the start button
        start = pygame.image.load(os.path.join(assets_folder, "MonsterGameAssets-024.png")).convert_alpha()
        start_rect = start.get_rect()

        # Place it in the middle
        self.button_rect = (
            self.position[0] + self.dimensions[0] // 2 - start_rect[2] // 2,
            self.position[1] + pos + 150,
            start_rect[2],
            start_rect[3]
        )
        self.image.blit(start, (self.button_rect[0], self.button_rect[1]))

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )
