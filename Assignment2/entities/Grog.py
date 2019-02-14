import os
import math
import random
import pygame
from pygame import gfxdraw
from entities.Colours import colours, possible_colours


class Grog(pygame.sprite.Sprite):
    font_size = 32

    hunger = [[7, 12], [5, 7], [3, 5]]

    def __init__(self, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.main_font = pygame.font.Font("assets/monogram.ttf", self.font_size)
        self.position = position
        self.dimensions = dimensions
        self.mouse_pos = (0, 0)
        self.image = None
        self.rect = ()
        self.requests = []
        self.set_image()

    def set_image(self):
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/large')
        self.image = pygame.Surface(self.dimensions)
        self.image.fill(colours["grog"])

        # Load the mouth image
        mouth = pygame.image.load(os.path.join(assets_folder, "MonsterGameAssets-019.png")).convert()
        mouth = pygame.transform.scale(mouth, self.dimensions)
        mouth_rect = mouth.get_rect()
        trans_color = mouth.get_at((0, 0))
        mouth.set_colorkey(trans_color)

        # Place it in the middle
        self.image.blit(mouth, mouth_rect)

        # Draw the eyes
        left_eye = pygame.Surface((50, 50))
        gfxdraw.filled_circle(
            left_eye,
            25,
            25,
            25,
            colours["white"]
        )
        gfxdraw.aacircle(
            left_eye,
            25,
            25,
            25,
            colours["white"]
        )
        gfxdraw.filled_circle(
            left_eye,
            25,
            40,
            5,
            colours["black"]
        )
        gfxdraw.aacircle(
            left_eye,
            25,
            40,
            5,
            colours["black"]
        )
        trans_color = left_eye.get_at((0, 0))
        left_eye.set_colorkey(trans_color)
        left_eye_pos = (
            (self.dimensions[0] / 2 - mouth_rect[2] / 2) + 10,
            25
        )

        right_eye = left_eye.copy()
        right_eye_pos = (
            (self.dimensions[0] / 2 + mouth_rect[2] / 2) - 60,
            25
        )
        trans_color = right_eye.get_at((0, 0))
        right_eye.set_colorkey(trans_color)

        # Rotate the eyes to place the cursor
        left_eye = pygame.transform.rotate(
            left_eye,
            -(math.atan2(
                left_eye_pos[1] - self.mouse_pos[1],
                left_eye_pos[0] - self.mouse_pos[0]
            )) * 180 / math.pi + 270
        )
        right_eye = pygame.transform.rotate(
            right_eye,
            -(math.atan2(
                right_eye_pos[1] - self.mouse_pos[1],
                right_eye_pos[0] - self.mouse_pos[0]
            )) * 180 / math.pi + 270
        )

        # Draw the two eyes
        self.image.blit(left_eye, left_eye_pos)
        self.image.blit(right_eye, right_eye_pos)

        # Draw the demands if any
        if len(self.requests) > 0:
            pos = -1
            for request in self.requests:
                gfxdraw.filled_circle(
                    self.image,
                    int(self.dimensions[0] / 2 + 60 * pos),
                    120,
                    20,
                    colours.get(request["color"]),
                )
                gfxdraw.aacircle(
                    self.image,
                    int(self.dimensions[0] / 2 + 60 * pos),
                    120,
                    20,
                    colours.get(request["color"]),
                )

                text = self.main_font.render(
                    str(request["quantity"]),
                    1,
                    colours["white"] if request["color"] != colours["yellow"] else colours["black"]
                )
                text_rect = text.get_rect()
                self.image.blit(text, (
                    int(self.dimensions[0] / 2 + 60 * pos) - text_rect[3] // 2 + 5, 105
                ))
                pos += 1

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )

    def change_mouse_pos(self, mouse_pos):
        self.mouse_pos = mouse_pos
        self.set_image()

    def determine_meal(self):
        self.requests.clear()
        colours = possible_colours.copy()
        random.shuffle(colours)

        self.requests.append({
            "color": colours[0],
            "quantity": random.randint(self.hunger[0][0], self.hunger[0][1]),
        })

        self.requests.append({
            "color": colours[1],
            "quantity": random.randint(self.hunger[1][0], self.hunger[1][1]),
        })

        self.requests.append({
            "color": colours[2],
            "quantity": random.randint(self.hunger[2][0], self.hunger[2][1]),
        })
        return self.requests

    def demands_met(self, balls):
        given = []

        for request in self.requests:
            given.append({
                "color": request["color"],
                "quantity": request["quantity"],
                "met": False,
            })

        for ball in balls:
            for request in given:
                if colours[request["color"]] == ball.colour and request["quantity"] <= ball.number:
                    request["met"] = True

        for request in given:
            if not request["met"]:
                return False

        return True
