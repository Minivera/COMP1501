import pygame


class Tower:
    max_level = 3

    def __init__(self, position_in_grid, square_size, attack_range, damage, attack_speed):
        self.position = (
            position_in_grid[0] * square_size[0] + square_size[0] // 2,
            position_in_grid[1] * square_size[1] + square_size[1] // 2,
        )
        self.square_size = square_size
        self.attack_range = (
                attack_range * square_size[0],
                attack_range * square_size[1],
        )
        self.damage = damage
        self.attack_speed = attack_speed
        self.level = 1
        self.effect = None
        self.frame = 0

    def find_target(self, enemies):
        range_rect = pygame.Rect(0, 0, self.attack_range[0] * 2, self.attack_range[1] * 2)
        range_rect.center = self.position
        for enemy in enemies:
            if range_rect.collidepoint(enemy.position[0], enemy.position[1]) and enemy.exists:
                return enemy

        return None

    def should_fire(self):
        return self.frame == self.attack_speed

    def upgrade(self):
        if self.level == self.max_level:
            return
        self.level += 1
        self.attack_range = (
            self.attack_range[0] + 1 * self.square_size[0],
            self.attack_range[1] + 1 * self.square_size[1],
        )
        self.damage += self.damage
        self.attack_speed += 5
        return

    def update(self):
        self.frame = self.frame + 1 if self.frame <= self.attack_speed else 0
        return
