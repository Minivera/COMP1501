import pygame
from pygame import gfxdraw
from entities.Colours import colours


class Ball(pygame.sprite.Sprite):
    base_radius = 40

    surface_size = 100

    animation_speed = 1

    speed_boost = 5

    focused_width = 2

    font_size = 32

    def __init__(self, colour, number, scale, position):
        pygame.sprite.Sprite.__init__(self)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.colour = colours[colour]
        self.number = number
        self.scale = scale
        self.position = position
        self.velocity = (0, 0)
        self.current_radius = int(self.base_radius * scale)
        self.focused = False
        self.moving = False
        self.resizing = False
        self.exists = True
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        if self.scale <= 0:
            return

        self.image = pygame.Surface((self.surface_size, self.surface_size))
        gfxdraw.filled_circle(
            self.image,
            self.surface_size // 2,
            self.surface_size // 2,
            self.current_radius,
            self.colour
        )
        gfxdraw.aacircle(
            self.image,
            self.surface_size // 2,
            self.surface_size // 2,
            self.current_radius,
            self.colour
        )

        if self.focused:
            # If focused, draw a white outline around the ball
            gfxdraw.aacircle(
                self.image,
                self.surface_size // 2,
                self.surface_size // 2,
                self.current_radius - 1,
                colours["white"],
            )
            gfxdraw.aacircle(
                self.image,
                self.surface_size // 2,
                self.surface_size // 2,
                self.current_radius,
                colours["white"],
            )

        # Render the text
        text = self.main_font.render(
            str(self.number),
            1,
            colours["white"] if self.colour != colours["yellow"] else colours["black"]
        )
        text_rect = text.get_rect()
        self.image.blit(text, (self.surface_size // 2 - text_rect[2] // 2, self.surface_size // 2 - text_rect[3] // 2))

        # Set the image's rectangle
        trans_color = self.image.get_at((0, 0))
        self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def change_color(self, colour):
        self.colour = colours[colour]
        self.set_image()

    def seek_to(self, target):
        target_pos = target.position
        # Check if currently at the same position of the ball target
        if isinstance(target, Ball) and self.collides_with(target):
            self.velocity = (0, 0)
            self.moving = False
        elif not isinstance(target, Ball) and pygame.Rect(target.rect).contains(pygame.Rect(self.rect)):
            # if the target is not a ball, but we still collide with it
            self.velocity = (0, 0)
            self.moving = False
        elif not isinstance(target, Ball):
            # otherwise, if the target is not a ball, set the target position to the center
            target_pos = target.image.get_rect().center

        # If not, move the ball towards the current position of the target
        steps_number = max(abs(target_pos[0] - self.position[0]), abs(target_pos[1] - self.position[1]))

        dx = float(target_pos[0] - self.position[0]) / steps_number
        dy = float(target_pos[1] - self.position[1]) / steps_number
        self.velocity = (dx * self.speed_boost, dy * self.speed_boost)
        self.moving = dx != 0 or dy != 0

    def collides_with(self, target):
        # Check if the distance between the two center is small or equal to the sum of the radii
        return (target.position[0] - self.position[0]) ** 2 + (target.position[1] - self.position[1]) ** 2\
            < (target.current_radius + self.current_radius) ** 2

    def update(self):
        pygame.sprite.Sprite.update(self)

        if self.scale <= 0:
            return

        # If the ball is still resizing
        if self.current_radius > int(self.base_radius * self.scale):
            self.current_radius = max(self.current_radius - self.animation_speed, int(self.base_radius * self.scale))
            self.resizing = True
        elif self.current_radius < int(self.base_radius * self.scale):
            self.current_radius = min(self.current_radius + self.animation_speed, int(self.base_radius * self.scale))
            self.resizing = True
        else:
            self.resizing = False

        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1],
        )

        self.set_image()
