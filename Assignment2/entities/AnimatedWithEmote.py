import pygame
from entities.Animated import Animated
from entities.Emote import Emote

intended_margin = 10


class AnimatedWithEmote(pygame.sprite.Sprite):
    def __init__(self, unit_type, state, animation_length, emote, scale, position, dimensions, orientation=0):
        pygame.sprite.Sprite.__init__(self)
        self.unit_type = unit_type
        self.state = state
        self.frame = 0
        self.anim_length = animation_length
        self.scale = scale
        self.position = position
        self.dimensions = dimensions
        self.initial_position = position
        self.orientation = orientation
        self.emote = emote
        self.entity = Animated(
            self.unit_type,
            self.state,
            self.anim_length,
            self.scale,
            (0, 0),
            self.orientation
        )
        self.emote_entity = Emote(self.emote, 2, (0, 0))
        self.image = None
        self.rect = ()
        self.set_image()

    def set_image(self):
        # Create a new surface to combine the sprites into
        self.image = pygame.Surface(self.dimensions)
        self.image.fill((255, 255, 255))

        # Calculate the position of the entity and emote in the surface if necessary
        entity_rect = self.__get_positions()

        # Blit the two sprites into the surface
        if self.emote:
            # Start by the emote if it exists
            self.emote_entity.position = (
                self.dimensions[0] / 2 - self.emote_entity.rect[0] / 2,
                entity_rect[1],
            )
            self.image.blit(self.emote_entity.image, self.emote_entity.position)

            # Then do the normal entity
            self.emote_entity.position = (
                entity_rect[0],
                entity_rect[1] + self.emote_entity.rect[1],
            )
            self.image.blit(self.entity.image, self.entity.position)
        else:
            # Just do the normal entity if no emote exists
            self.entity.position = (
                entity_rect[0],
                entity_rect[1],
            )
            self.image.blit(self.entity.image, self.entity.position)

        trans_color = self.image.get_at((0, 0))
        #self.image.set_colorkey(trans_color)
        self.rect = self.image.get_rect()
        self.rect = (
            self.position[0],
            self.position[1],
            self.rect[2],
            self.rect[3],
        )

    def __get_positions(self):
        entity_rect = self.entity.rect
        if self.emote:
            emote_rect = self.emote_entity.rect
            entity_rect = [
                entity_rect[2],
                entity_rect[3] + emote_rect[3],
            ]
        return [
            self.dimensions[0] / 2 - entity_rect[2] / 2,
            self.dimensions[1] - intended_margin - entity_rect[3],
        ]

    def change_state(self, new_state):
        self.state = new_state
        self.entity.change_state(new_state)
        self.set_image()

    def change_type(self, new_type):
        self.unit_type = new_type
        self.entity.change_type(new_type)
        self.set_image()

    def change_emote(self, new_emote):
        self.emote = new_emote
        self.emote_entity.change_type(new_emote)
        self.set_image()

    def animate(self):
        self.entity.animate()
        self.emote_entity.animate()
        self.set_image()

    def rotate(self, orientation):
        self.orientation = orientation
        self.entity.rotate(orientation)
        self.set_image()

    def reset_position(self):
        self.position = self.initial_position
        self.set_image()
