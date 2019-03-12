import pygame
from pygame import gfxdraw
from constants.Colours import colours


class UpgradeMenu(pygame.sprite.Sprite):
    font_size = 32

    radius_from_square = 100
    button_size = (80, 30)
    margin = 10

    def __init__(self, position, square_size, current_money):
        pygame.sprite.Sprite.__init__(self)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.position = position
        self.radius = square_size // 2 + self.radius_from_square
        self.image = None
        self.is_open = False
        self.saved_square = None
        self.saved_money = current_money
        self.tower_type = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface(
            (self.radius * 2, self.radius * 2),
            pygame.SRCALPHA,
            32,
        )
        self.image = self.image.convert_alpha()
        self.image.fill((0, 0, 0, 0))

        if not self.is_open:
            return

        # Render the circle menu
        gfxdraw.filled_circle(
            self.image,
            self.radius,
            self.radius,
            self.radius,
            colours["circle_menu"],
        )
        gfxdraw.aacircle(
            self.image,
            self.radius,
            self.radius,
            self.radius,
            colours["circle_menu"],
        )

        # Render the upgrade button
        button_rect = pygame.Rect(0, 0, self.button_size[0], self.button_size[0])
        button_rect.center = (self.radius, self.button_size[1] // 2 + self.margin)
        pygame.draw.rect(self.image, colours["button"], button_rect)
        # Render the update label
        text = self.main_font.render("Upgrade", 1, colours["text_contrasted"])
        text_rect = text.get_rect(center=(self.radius, self.button_size[1] // 2 + self.margin))
        self.image.blit(text, text_rect)
        # Draw the cost
        text = self.main_font.render(
            str(self.tower_type["upgrade_cost"]) + "$",
            1,
            colours["text_contrasted"] if self.tower_type["upgrade_cost"] <= self.saved_money else colours["text_gray"],
        )
        text_rect = text.get_rect(center=(self.radius, self.button_size[1] + self.margin * 2))
        self.image.blit(text, text_rect)

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        return

    def hit_menu(self, mouse_pos):
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = self.position
        return rect.collidepoint(mouse_pos[0], mouse_pos[1])

    def check_click(self, mouse_pos):
        rect = pygame.Rect(0, 0, self.radius * 2, self.radius * 2)
        rect.center = self.position
        # Transpose the mouse position to be inside the circle menu
        internal_pos = (
            mouse_pos[0] - rect[0],
            mouse_pos[1] - rect[1],
        )

        # Check if hitting the button
        souvenir_rect = pygame.Rect(0, 0, self.button_size[0], self.button_size[1])
        souvenir_rect.center = (self.radius, self.button_size[1] // 2 + self.margin)
        if souvenir_rect.collidepoint(internal_pos[0], internal_pos[1]):
            return True

        return False

    def set_clicked_square(self, square):
        self.saved_square = square
        return

    def set_position(self, new_position):
        self.position = new_position
        self.set_image()
        return

    def set_money(self, new_money):
        self.saved_money = new_money
        self.set_image()
        return

    def set_tower_type(self, new_type):
        self.tower_type = new_type
        self.set_image()
        return

    def open(self):
        self.is_open = True
        self.set_image()
        return

    def close(self):
        self.is_open = False
        self.set_image()
        return
