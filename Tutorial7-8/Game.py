import pygame
from entities.Statusbar import Statusbar
from entities.Map import Map
from entities.Enemy import Enemy
from constants.Types import types

STATE_NONE = -1
STATE_MENU = 0
STATE_GAME = 1

BUTTON_LEFT = 1
BUTTON_RIGHT = 3


class Game:
    status_bar_size = 40

    map_size = 26

    enemies_per_difficulty = 2
    money_per_difficulty = 20

    def __init__(self, screen_size):
        self.is_running = False
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.grid = [[]]
        self.starting_square = None
        self.ending_square = None
        self.enemies_path = []
        self.difficulty = 1
        self.status_bar = Statusbar((screen_size[0], self.status_bar_size), (0, 0), "Tower Builder", "00", "0")
        self.map_entity = None
        self.generate_map()
        self.generate_wave()
        self.decide_enemies_path()

    def generate_map(self):
        self.grid = []

        path_pos = self.map_size // 2
        for i in range(0, self.map_size, 1):
            self.grid.append([])
            for j in range(0, self.map_size, 1):
                self.grid[i].append({
                    "type": types["path"] if j == path_pos else types["grass"],
                    "starting_square": False,
                    "ending_square": False,
                    "position": (i, j),
                    "entities": [],
                })
                if i == self.map_size and j == self.map_size // 2:
                    self.starting_square = self.grid[i][j]
                if i == 0 and j == self.map_size // 2:
                    self.ending_square = self.grid[i][j]

        self.map_entity = Map(
            (self.screen_size[0], self.screen_size[1] - self.status_bar_size),
            (0, self.status_bar_size),
            self.grid,
        )
        return

    def decide_enemies_path(self):
        self.enemies_path = []
        current_square = self.starting_square

        while current_square != self.ending_square:
            pos = current_square["position"]
            self.enemies_path.append(current_square)
            current_square = self.grid[pos[0]][pos[1] - 1]

        self.enemies_path.append(self.ending_square)
        return

    def generate_wave(self):
        for i in range(0, self.difficulty):
            for j in range(0, self.enemies_per_difficulty):
                self.starting_square["entities"].append(Enemy(
                    self.starting_square["position"],
                    self.map_entity.square_size,
                    self.money_per_difficulty * i,
                ))
        return

    def start(self):
        self.is_running = True
        return

    def handle_input(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                self.end_game()
                return
        return

    def render(self, sprites):
        # render stuff
        self.screen.fill((0, 0, 0))

        sprites.add(self.status_bar)
        sprites.add(self.map_entity)

        for row in self.grid:
            for column in row:
                for entity in column["entities"]:
                    sprites.add(entity)

        sprites.draw(self.screen)
        return

    def update(self):
        for i in range(len(self.enemies_path) - 1, 0, -1):
            square = self.enemies_path[i]
            # If all enemies in this square have moved and there are enemies in the previous square, move over
            moved = True
            for entity in square["entities"]:
                if entity.is_moving():
                    moved = False
                    break

            if moved and i - 1 > 0 and len(self.enemies_path[i - 1]["entities"]) > 0:
                other_square = self.enemies_path[i - 1]
                for entity in other_square["entities"]:
                    if not entity.is_moving():
                        entity.move_to(other_square["position"])


        for row in self.grid:
            for column in row:
                for entity in column["entities"]:
                    entity.update_entity()
        return

    def clean(self):
        return

    def end_game(self):
        self.is_running = False
        return
