from entities.AnimatedWithEmote import AnimatedWithEmote, Emote


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

    def __init__(self, unit_type, emote, orientation, square_size, grid_left_corner, location_on_grid):
        self.square_size = square_size
        self.grid_left_corner = grid_left_corner
        self.location = location_on_grid
        self.position = self.__get_pos(location_on_grid)
        self.initial_position = self.__get_pos(location_on_grid)
        self.future_position = self.__get_pos(location_on_grid)
        self.unit_type = unit_type
        self.emote = emote
        self.orientation = orientation
        self.entity = None
        self.set_entity("idle")

    def set_entity(self, state):
        self.entity = AnimatedWithEmote(
            self.images[self.unit_type],
            state,
            self.animations[state],
            self.emote,
            self.scale,
            self.position,
            (self.square_size, self.square_size),
            self.orientation
        )

    def __get_pos(self, position):
        return (
            self.grid_left_corner[0] + position[0] * self.square_size,
            self.grid_left_corner[1] + position[1] * self.square_size,
        )

    def rotate(self, orientation):
        self.orientation = orientation
        self.entity.rotate(orientation)

    def run_to(self, new_location):
        self.location = new_location
        self.future_position = self.__get_pos(new_location)
        self.entity.change_state("run")

    def move_to(self, new_location):
        self.location = new_location
        self.position = self.__get_pos(new_location)
        self.future_position = self.__get_pos(new_location)

    def reset_position(self):
        self.entity.reset_position()
        self.position = self.initial_position
        self.future_position = self.initial_position

    def change_emote(self, new_emote):
        if self.emote not in Emote.emote_positions:
            self.emote = False
            self.entity.change_type(False)
            return
        self.emote = new_emote
        self.entity.change_type(new_emote)

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

    def clean(self):
        self.entity.kill()
