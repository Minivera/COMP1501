import pygame
from constants.Colours import colours


class Enemy(pygame.sprite.Sprite):
    speed = 1

    health_bar_size = 3

    modifier_length = 120

    def __init__(self, position_in_grid, square_size, difficulty, money, path):
        pygame.sprite.Sprite.__init__(self)
        self.position = (
            position_in_grid[0] * square_size[0] + square_size[0] // 2,
            position_in_grid[1] * square_size[1] + square_size[1] // 2,
        )
        self.square_size = square_size
        self.difficulty = difficulty
        self.start_money = money
        self.money = money
        self.path = path
        self.moving = False
        self.exists = True
        self.current_square = 0
        self.speed_modifier = 1
        self.modifier_applied = False
        self.frame = 0
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface((self.square_size[0] // 2, self.square_size[1] // 2))

        self.image.fill(colours["enemy"])

        # Draw a health bar
        health_percent = self.money / self.start_money
        health_rect = pygame.Rect(
            int((self.square_size[0] // 2) * (1 - health_percent)),
            (self.square_size[1] // 2) - self.health_bar_size,
            int((self.square_size[0] // 2) * health_percent),
            self.health_bar_size,
        )
        pygame.draw.rect(self.image, colours["health"], health_rect)

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        return

    def set_money(self, new_money):
        self.money = new_money
        self.set_image()
        return

    def damage(self, damage):
        self.set_money(self.money - damage)
        if self.money <= 0:
            self.exists = False
        return

    def apply_effect(self, modifier):
        if modifier is None:
            return
        self.frame = 0
        self.modifier_applied = True
        self.speed_modifier = modifier
        return

    def set_path(self, new_path):
        self.path = new_path
        return

    def update(self):
        if not self.exists:
            return

        if self.modifier_applied:
            self.frame += 1
            if self.frame >= self.modifier_length:
                self.modifier_applied = False
                self.speed_modifier = 1

        square_pos = (
            self.path[self.current_square]["position"][0] * self.square_size[0] + self.square_size[0] // 2,
            self.path[self.current_square]["position"][1] * self.square_size[1] + self.square_size[1] // 2,
        )
        if square_pos[0] in range(int(self.position[0]) - 1, int(self.position[0]) + 2, 1) and \
                square_pos[1] in range(int(self.position[1]) - 1, int(self.position[1]) + 2, 1):
            self.current_square += 1
            if self.current_square >= len(self.path):
                self.exists = False
            return

        steps_number = max(abs(square_pos[0] - self.position[0]), abs(square_pos[1] - self.position[1]))

        dx = (square_pos[0] - self.position[0]) / steps_number
        dy = (square_pos[1] - self.position[1]) / steps_number

        self.position = (
            self.position[0] + dx * (self.speed * self.speed_modifier),
            self.position[1] + dy * (self.speed * self.speed_modifier),
        )
        self.set_image()
