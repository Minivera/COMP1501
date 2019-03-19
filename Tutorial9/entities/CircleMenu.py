import pygame
from pygame import gfxdraw
from constants.Colours import colours
from constants.Towers import souvenir_shop, flower_shop, clothing_shop, food_shop


class CircleMenu(pygame.sprite.Sprite):
    font_size = 32

    radius_from_square = 100
    shop_size = 40
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

        # Render the souvenir Shop, top
        souvenir_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        souvenir_rect.center = (self.radius, self.shop_size // 2 + self.margin)
        pygame.draw.rect(self.image, colours["shop"], souvenir_rect)
        # Draw the cost
        text = self.main_font.render(
            str(souvenir_shop["cost"]) + "$",
            1,
            colours["text_contrasted"] if souvenir_shop["cost"] <= self.saved_money else colours["text_gray"],
        )
        text_rect = text.get_rect(center=(self.radius, self.shop_size + self.margin * 2))
        self.image.blit(text, text_rect)

        # Render the flower Shop, right
        flower_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        flower_rect.center = (self.radius * 2 - self.shop_size // 2 - self.margin, self.radius)
        pygame.draw.rect(self.image, colours["shop"], flower_rect)
        # Draw the cost
        text = self.main_font.render(
            str(flower_shop["cost"]) + "$",
            1,
            colours["text_contrasted"] if flower_shop["cost"] <= self.saved_money else colours["text_gray"],
        )
        text_rect = text.get_rect(center=(
            self.radius * 2 - self.shop_size // 2 - self.margin,
            self.radius + self.shop_size // 2 + self.margin,
        ))
        self.image.blit(text, text_rect)

        # Render the clothing Shop, bottom
        clothing_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        clothing_rect.center = (self.radius, self.radius * 2 - self.shop_size // 2 - self.margin * 2)
        pygame.draw.rect(self.image, colours["shop"], clothing_rect)
        # Draw the cost
        text = self.main_font.render(
            str(clothing_shop["cost"]) + "$",
            1,
            colours["text_contrasted"] if clothing_shop["cost"] <= self.saved_money else colours["text_gray"],
        )
        text_rect = text.get_rect(center=(self.radius, self.radius * 2 - self.margin))
        self.image.blit(text, text_rect)

        # Render the food Shop, left
        food_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        food_rect.center = (self.shop_size // 2 + self.margin, self.radius)
        pygame.draw.rect(self.image, colours["shop"], food_rect)
        # Draw the cost
        text = self.main_font.render(
            str(food_shop["cost"]) + "$",
            1,
            colours["text_contrasted"] if food_shop["cost"] <= self.saved_money else colours["text_gray"],
        )
        text_rect = text.get_rect(center=(
            self.shop_size // 2 + self.margin,
            self.radius + self.shop_size // 2 + self.margin,
        ))
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

        # Check if hitting the souvenir shop
        souvenir_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        souvenir_rect.center = (self.radius, self.shop_size // 2 + self.margin)
        if souvenir_rect.collidepoint(internal_pos[0], internal_pos[1]):
            return souvenir_shop

        # Check if hitting the flower shop
        flower_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        flower_rect.center = (self.radius * 2 - self.shop_size // 2 - self.margin, self.radius)
        if flower_rect.collidepoint(internal_pos[0], internal_pos[1]):
            return flower_shop

        # Check if hitting the clothing shop
        clothing_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        clothing_rect.center = (self.radius, self.radius * 2 - self.shop_size // 2 - self.margin * 2)
        if clothing_rect.collidepoint(internal_pos[0], internal_pos[1]):
            return clothing_shop

        # Check if hitting the clothing shop
        food_rect = pygame.Rect(0, 0, self.shop_size, self.shop_size)
        food_rect.center = (self.shop_size // 2 + self.margin, self.radius)
        if food_rect.collidepoint(internal_pos[0], internal_pos[1]):
            return food_shop

        return None

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

    def open(self):
        self.is_open = True
        self.set_image()
        return

    def close(self):
        self.is_open = False
        self.set_image()
        return
