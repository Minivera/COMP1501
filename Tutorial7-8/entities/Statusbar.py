import pygame
from constants.Colours import colours


class Statusbar(pygame.sprite.Sprite):
    font_size = 32

    margin = 20

    def __init__(self, dimensions, position, title, money, support):
        pygame.sprite.Sprite.__init__(self)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.dimensions = dimensions
        self.position = position
        self.title = title
        self.money = money
        self.support = "{:0>2d}".format(support)
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface(self.dimensions)
        self.image.fill(colours["status_bar"])

        # Render the title
        title = self.main_font.render(
            self.title,
            1,
            colours["text_contrasted"],
        )
        title_rect = title.get_rect()
        self.image.blit(
            title,
            (self.dimensions[0] // 2 - title_rect[2] // 2, self.dimensions[1] // 2 - title_rect[3] // 2),
        )

        # Render the popular support
        support = self.main_font.render(
            "Support: " + self.support + "%",
            1,
            colours["text_contrasted"],
        )
        support_rect = support.get_rect()
        self.image.blit(
            support,
            (self.dimensions[0] - support_rect[2] - self.margin, self.dimensions[1] // 2 - support_rect[3] // 2),
        )

        # Render the money
        money = self.main_font.render(
            "money: " + self.money + "$",
            1,
            colours["text_contrasted"],
        )
        money_rect = money.get_rect()
        self.image.blit(
            money,
            (
                self.dimensions[0] - money_rect[2] - self.margin * 2 - support_rect[2],
                self.dimensions[1] // 2 - money_rect[3] // 2,
            ),
        )

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )
        return

    def set_support(self, new_support):
        self.support = "{:0>2d}".format(new_support)
        self.set_image()
        return

    def set_money(self, new_money):
        self.money = str(new_money)
        self.set_image()
        return
