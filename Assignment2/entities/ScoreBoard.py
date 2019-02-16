import pygame
from entities.Colours import colours


class ScoreBoard(pygame.sprite.Sprite):
    font_size = 32

    def __init__(self, score, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.position = position
        self.dimensions = dimensions
        self.score = score
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface(self.dimensions)
        self.image.fill(colours["gray"])

        # Draw the text in the center right
        text = self.main_font.render(
            str(self.score),
            1,
            colours["white"]
        )
        text_rect = text.get_rect()
        self.image.blit(text, (
            self.dimensions[0] - text_rect[2] - 15,
            self.dimensions[1] // 2 - text_rect[3] // 2,
        ))

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )

    def change_score(self, score):
        self.score = score
        self.set_image()
