import pygame
import os

block_top_left = (6, 13, 15, 19)
block_top_middle = (17, 13, 73, 19)
block_top_right = (75, 13, 83, 19)
block_middle_left = (6, 21, 15, 43)
block_middle = (17, 21, 73, 43)
block_middle_right = (75, 21, 83, 43)
block_bottom_left = (6, 45, 15, 53)
block_bottom_middle = (17, 45, 73, 53)
block_bottom_right = (75, 45, 83, 53)
scale = 2


class UIBlock(pygame.sprite.Sprite):
    def __init__(self, dimensions, position):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.dimensions = dimensions
        self.initial_position = position
        self.scale = scale
        self.image = ""
        self.rect = ()
        self.set_image()

    def set_image(self):
        # Fetch the sprite sheet
        assets_folder = os.path.join(os.path.dirname(__file__), '../assets/ui/ui_split.png')
        sheet = pygame.image.load(assets_folder)

        # Draw the base surface
        self.image = pygame.Surface(self.dimensions)

        # Calculate the number of middle element wide
        count_wide = 0
        current_width = self.dimensions[0] - self.__get_width(block_top_left) - self.__get_width(block_top_right)
        while current_width > self.__get_width(block_middle):
            count_wide += 1
            current_width -= self.__get_width(block_middle)

        # Calculate the number of middle element high
        count_high = 0
        current_height = self.dimensions[1] - self.__get_height(block_top_left) - self.__get_height(block_bottom_left)
        while current_height > self.__get_height(block_middle):
            count_high += 1
            current_height -= self.__get_height(block_middle)

        # Start with the top left corner
        top_corner = sheet.subsurface(
            pygame.Rect(
                block_top_left[0],
                block_top_left[1],
                self.__get_width(block_top_left),
                self.__get_height(block_top_left)
            )
        )
        self.image.blit(top_corner, (0, 0))

        # Add the middle top element, ignore any overflow
        for i in range(0, count_wide):
            middle = sheet.subsurface(
                pygame.Rect(
                    block_top_middle[0],
                    block_top_middle[1],
                    self.__get_width(block_top_middle),
                    self.__get_height(block_top_middle)
                )
            )
            self.image.blit(middle, (self.__get_width(block_top_left) + self.__get_width(block_top_middle) * i, 0))

        # Add the top right element
        right = sheet.subsurface(
            pygame.Rect(
                block_top_right[0],
                block_top_right[1],
                self.__get_width(block_top_right),
                self.__get_height(block_top_right)
            )
        )
        self.image.blit(right, (self.__get_width(block_top_left) + self.__get_width(block_top_middle) * count_wide, 0))

        # For the height of the block
        for i in range(0, count_high):
            # Add the middle left element
            left = sheet.subsurface(
                pygame.Rect(
                    block_middle_left[0],
                    block_middle_left[1],
                    self.__get_width(block_middle_left),
                    self.__get_height(block_middle_left)
                )
            )
            self.image.blit(left, (
                0,
                self.__get_height(block_top_left) + self.__get_height(block_middle_left) * i
            ))

            # Add as many middle element for the width, ignoring overflow
            for j in range(0, count_wide):
                middle = sheet.subsurface(
                    pygame.Rect(
                        block_middle[0],
                        block_middle[1],
                        self.__get_width(block_middle),
                        self.__get_height(block_middle)
                    )
                )
                self.image.blit(middle, (
                    self.__get_width(block_middle_left) + self.__get_width(block_middle) * j,
                    self.__get_height(block_top_middle) + self.__get_height(block_middle) * i
                ))

            # Add the middle right element
            right = sheet.subsurface(
                pygame.Rect(
                    block_middle_right[0],
                    block_middle_right[1],
                    self.__get_width(block_middle_right),
                    self.__get_height(block_middle_right)
                )
            )
            self.image.blit(right, (
                self.__get_width(block_middle_left) + self.__get_width(block_middle) * count_wide,
                self.__get_height(block_top_right) + self.__get_height(block_middle) * i
            ))

        # Add the bottom left element
        left = sheet.subsurface(
            pygame.Rect(
                block_bottom_left[0],
                block_bottom_left[1],
                self.__get_width(block_bottom_left),
                self.__get_height(block_bottom_left)
            )
        )
        self.image.blit(left, (
            0,
            self.__get_height(block_top_left) + self.__get_height(block_middle) * count_high
        ))

        # Add as many bottom element for the width, ignoring overflow
        for i in range(0, count_wide):
            middle = sheet.subsurface(
                pygame.Rect(
                    block_bottom_middle[0],
                    block_bottom_middle[1],
                    self.__get_width(block_bottom_middle),
                    self.__get_height(block_bottom_middle)
                )
            )
            self.image.blit(middle, (
                self.__get_width(block_bottom_left) + self.__get_width(block_bottom_middle) * i,
                self.__get_height(block_top_middle) + self.__get_height(block_middle) * count_high
            ))

        # Add the bottom right element
        right = sheet.subsurface(
            pygame.Rect(
                block_bottom_right[0],
                block_bottom_right[1],
                self.__get_width(block_bottom_right),
                self.__get_height(block_bottom_right)
            )
        )
        self.image.blit(right, (
            self.__get_width(block_bottom_left) + self.__get_width(block_bottom_middle) * count_wide,
            self.__get_height(block_top_right) + self.__get_height(block_middle) * count_high
        ))

        # Rescale the image
        self.image = pygame.transform.scale(
            self.image,
            (self.dimensions[0] * self.scale, self.dimensions[1] * self.scale)
        )

        # Set the image's rectangle
        self.rect = self.image.get_rect()
        self.rect = pygame.Rect(self.position[0], self.position[1], self.rect[2], self.rect[3])

    def __get_position(self, position, offset):
        return (
            position[0] + offset[0] * scale,
            position[1] + offset[1] * scale,
        )

    def __get_width(self, tup):
        return tup[2] - tup[0]

    def __get_height(self, tup):
        return tup[3] - tup[1]
