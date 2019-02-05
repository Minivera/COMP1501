from entities.Animated import Animated
from entities.Emote import Emote


class Unit:
    images = {
        "wizard": "wizzard_m",
        "knight": "knight_m",
        "thief": "elf_m",
        "orc": "orc_warrior",
        "goblin": "goblin",
    }

    animations = {
        "idle": 4,
        "run": 4,
        "hit": 1,
    }

    scale = 2

    run_speed = 2

    def __init__(self, unit_type, emote, orientation, left_corner, square_size, position):
        self.left_corner = left_corner
        self.square_size = square_size
        self.position = position
        self.initial_position = position
        self.future_position = position
        self.unit_type = unit_type
        self.emote = emote
        self.orientation = orientation
        self.entity = False
        self.emote_entity = False
        self.set_entity("idle")

    def set_entity(self, state):
        self.entity = Animated(
            self.images[self.unit_type],
            state,
            self.animations[state],
            self.scale,
            self.__get_pos(),
            self.orientation
        )
        self.emote_entity = Emote(self.emote, 2, self.__get_pos())

    def __get_pos(self):
        return (
            self.left_corner[0] + self.position[0] * self.square_size - self.square_size / 2,
            self.left_corner[1] + self.position[1] * self.square_size - self.square_size / 2,
        )

    def rotate(self, orientation):
        self.orientation = orientation
        self.entity.rotate(orientation)

    def run_to(self, new_position):
        self.future_position = new_position
        self.entity.change_state("run")

    def move_to(self, new_position):
        self.position = new_position
        self.future_position = new_position

    def reset_position(self):
        self.entity.reset_position()
        self.position = self.initial_position
        self.future_position = self.initial_position

    def change_emote(self, new_emote):
        if self.emote not in Emote.emote_positions:
            self.emote = False
            return
        self.emote = new_emote
        self.emote_entity.change_type(new_emote)

    def has_emote(self):
        return False if not self.emote or self.emote not in Emote.emote_positions else True

    def move_finished(self):
        return self.position == self.future_position

    def update(self):
        if not self.move_finished():
            movement_x = 0
            movement_y = 0
            if self.position[0] < self.future_position[0]:
                movement_x = self.run_speed
            elif self.position[0] > self.future_position[0]:
                movement_x = -self.run_speed
            if self.position[1] < self.future_position[1]:
                movement_y = self.run_speed
            elif self.position[1] > self.future_position[1]:
                movement_y = -self.run_speed

            self.position = (
                self.position[0] + movement_x,
                self.position[1] + movement_y,
            )
            self.entity.position = self.position
        else:
            self.entity.change_state("idle")

        self.entity.animate()
        self.emote_entity.animate()

    def clean(self):
        self.entity.kill()
        self.emote_entity.kill()
