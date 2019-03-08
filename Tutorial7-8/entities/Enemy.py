import pygame
from constants.Colours import colours


class Enemy(pygame.sprite.Sprite):
    speed = 10

    def __init__(self, position_in_grid, square_size, money):
        pygame.sprite.Sprite.__init__(self)
        self.position = (
            position_in_grid[0] * square_size[0] + square_size[0] // 2,
            position_in_grid[1] * square_size[1] + square_size[1] // 2,
        )
        self.intended_pos = position_in_grid
        self.square_size = square_size
        self.money = money
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        self.image = pygame.Surface((self.square_size[0] // 2, self.square_size[1] // 2))

        self.image.fill(colours["enemy"])

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (
            self.position[0] * self.square_size[0] + self.square_size[0] // 2,
            self.position[1] * self.square_size[1] + self.square_size[1] // 2,
        )
        return

    def set_money(self, new_money):
        self.money = new_money
        self.set_image()
        return

    def move_to(self, new_square):
        self.intended_pos = (
            new_square[0] * self.square_size[0] + self.square_size[0] // 2,
            new_square[1] * self.square_size[1] + self.square_size[1] // 2,
        )

    def is_moving(self):
        return self.position != self.intended_pos

    def update_entity(self):
        dx = 0
        dy = 0
        if self.position[0] > self.intended_pos[0]:
            dx = -min(self.speed, self.intended_pos[0] - self.position[0])
        elif self.position[0] < self.intended_pos[0]:
            dx = min(self.speed, self.intended_pos[0] - self.position[0])

        if self.position[1] > self.intended_pos[1]:
            dy = -self.speed if self.position[1] - self.intended_pos[1] > self.speed else self.position[1] - self.intended_pos[1]
        elif self.position[0] < self.intended_pos[0]:
            dy = self.speed if self.position[1] - self.intended_pos[1] > self.speed else self.position[1] - self.intended_pos[1]

        self.position = (
            self.position[0] + dx,
            self.position[1] + dy,
        )
        self.set_image()
