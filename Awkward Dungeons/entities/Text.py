import pygame


class Text(pygame.sprite.Sprite):
    def __init__(self, font_size, text, color, position, dimensions, center=False):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.initial_position = position
        self.dimensions = dimensions
        self.font_size = font_size
        self.text = text
        self.color = color
        self.center = center
        self.image = ""
        self.rect = ()
        self.set_image()

    def set_image(self):
        # Render the text
        main_font = pygame.font.Font("assets/fonts/Awkward.ttf", self.font_size)
        text = main_font.render(self.text, 1, self.color)

        # Draw the text
        self.image = pygame.Surface(self.dimensions)
        self.image.blit(text, [0, 0])

        # Set the image's rectangle
        trans_color = self.image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        if self.center:
            self.rect.center = self.position
        else:
            self.rect = pygame.Rect(self.position[0], self.position[1], self.rect[2], self.rect[3])

    def reset_position(self):
        self.position = self.initial_position
