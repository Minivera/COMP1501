import pygame
from entities.Statusbar import Statusbar
from entities.CircleMenu import CircleMenu
from entities.UpgradeMenu import UpgradeMenu
from entities.Map import Map
from entities.Enemy import Enemy
from entities.towers.SouvenirShop import SouvenirShop
from entities.towers.ClothingShop import ClothingShop
from entities.towers.FoodShop import FoodShop
from entities.Bullet import Bullet
from constants.Types import types

STATE_NONE = -1
STATE_MENU = 0
STATE_GAME = 1

BUTTON_LEFT = 1
BUTTON_RIGHT = 3


class Game:
    status_bar_size = 40

    map_size = 25

    enemies_per_difficulty = 2
    money_per_difficulty = 40

    spawn_delay = 30

    rebuild_distance = 3

    def __init__(self, screen_size):
        self.is_running = False
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.map_surface = pygame.Surface(
            (self.screen_size[0], self.screen_size[1] - self.status_bar_size),
            pygame.SRCALPHA,
            32,
        )
        self.map_surface = self.map_surface.convert_alpha()
        self.screen_sprites = pygame.sprite.Group()
        self.map_sprites = pygame.sprite.Group()
        self.grid = [[]]
        self.starting_square = None
        self.ending_square = None
        self.enemies_path = []
        self.enemies = []
        self.to_spawn = []
        self.towers = []
        self.bullets = []
        self.frame = 0
        self.difficulty = 1
        self.popular_support = 100
        self.money = 450
        self.status_bar = Statusbar(
            (screen_size[0], self.status_bar_size),
            (0, 0),
            "Tower Builder",
            str(self.money),
            self.popular_support,
        )
        self.map_entity = None
        self.generate_map()
        self.decide_enemies_path()
        self.generate_wave()
        self.circle_menu = CircleMenu((0, 0), self.map_entity.square_size[0], self.money)
        self.upgrade_menu = UpgradeMenu((0, 0), self.map_entity.square_size[0], self.money)

    def generate_map(self):
        self.grid = []

        path_pos = self.map_size // 2
        for i in range(0, self.map_size + 1, 1):
            self.grid.append([])
            for j in range(0, self.map_size + 1, 1):
                self.grid[i].append({
                    "type": types["path"] if j == path_pos else types["grass"],
                    "starting_square": False,
                    "ending_square": False,
                    "position": (j, i),
                    "next": [],
                    "previous": [],
                })
                if i == self.map_size and j == self.map_size // 2:
                    self.starting_square = self.grid[i][j]
                    self.grid[i][j]["starting_square"] = True
                if i == 0 and j == self.map_size // 2:
                    self.ending_square = self.grid[i][j]
                    self.grid[i][j]["ending_square"] = True

        # Create the next and previous arrays
        for i in range(self.map_size, -1, -1):
            for j in range(self.map_size, -1, -1):
                if self.grid[i][j]["type"] == types["path"]:
                    # Top square
                    if i > 0 and self.grid[i - 1][j]["type"] == types["path"]:
                        self.grid[i][j]["next"].append(self.grid[i - 1][j]["position"])
                        self.grid[i - 1][j]["previous"].append(self.grid[i][j]["position"])

        self.map_entity = Map(
            (self.map_surface.get_rect()[2], self.map_surface.get_rect()[3]),
            (0, self.status_bar_size),
            self.grid,
        )
        return

    def decide_enemies_path(self):
        self.enemies_path = []
        current_square = self.starting_square

        while current_square != self.ending_square:
            self.enemies_path.append(current_square)
            next_pos = current_square["next"][0]
            current_square = self.grid[next_pos[1]][next_pos[0]]

        self.enemies_path.append(self.ending_square)
        return

    def generate_wave(self):
        self.enemies.append(Enemy(
            self.starting_square["position"],
            self.map_entity.square_size,
            1,
            self.money_per_difficulty * 1,
            self.enemies_path,
        ))
        for i in range(1, self.difficulty + 1):
            for j in range(0, self.enemies_per_difficulty):
                self.to_spawn.append(Enemy(
                    self.starting_square["position"],
                    self.map_entity.square_size,
                    i,
                    self.money_per_difficulty * i,
                    self.enemies_path,
                ))
        return

    def start(self):
        self.is_running = True
        return

    def handle_input(self):
        events = pygame.event.get()
        mouse_pos = pygame.mouse.get_pos()
        map_mouse_pos = (
            mouse_pos[0],
            mouse_pos[1] - self.status_bar_size,
        )

        for event in events:
            if event.type == pygame.QUIT:
                self.end_game()
                return

            if event.type == pygame.MOUSEBUTTONUP:
                clicked_square = self.map_entity.square_under_mouse(map_mouse_pos)
                if event.button == BUTTON_RIGHT and clicked_square["type"] == types["path"]:
                    self.circle_menu.set_position(map_mouse_pos)
                    self.circle_menu.set_clicked_square(clicked_square)
                    self.circle_menu.open()
                    continue
                if event.button == BUTTON_RIGHT and clicked_square["type"] != types["path"] and\
                        clicked_square["type"] != types["grass"]:
                    self.upgrade_menu.set_position(map_mouse_pos)
                    self.upgrade_menu.set_clicked_square(clicked_square)
                    for tower in self.towers:
                        if tower.grid_position == clicked_square["position"]:
                            self.upgrade_menu.set_tower_type(tower.tower_type)
                            self.upgrade_menu.set_level(tower.level)
                            break
                    self.upgrade_menu.open()
                    continue
                if event.button == BUTTON_LEFT:
                    if self.circle_menu.is_open and self.circle_menu.hit_menu(map_mouse_pos):
                        clicked_shop = self.circle_menu.check_click(map_mouse_pos)
                        if clicked_shop is not None:
                            self.build_tower(clicked_shop)
                            self.circle_menu.close()
                            continue
                    elif self.circle_menu.is_open:
                        self.circle_menu.close()
                        continue
                    if self.upgrade_menu.is_open and self.upgrade_menu.hit_menu(map_mouse_pos):
                        if self.upgrade_menu.check_click(map_mouse_pos):
                            self.upgrade_tower()
                            self.upgrade_menu.close()
                            continue
                    elif self.upgrade_menu.is_open:
                        self.upgrade_menu.close()
                        continue
        return

    def render(self):
        # render stuff
        self.screen.fill((0, 0, 0))
        self.map_surface.fill((0, 0, 0, 0))

        self.screen_sprites.add(self.status_bar)
        self.screen_sprites.add(self.map_entity)

        if self.circle_menu.is_open:
            self.map_sprites.add(self.circle_menu)

        if self.upgrade_menu.is_open:
            self.map_sprites.add(self.upgrade_menu)

        for entity in self.towers:
            self.map_sprites.add(entity)

        for entity in self.enemies:
            self.map_sprites.add(entity)

        for entity in self.bullets:
            self.map_sprites.add(entity)

        self.screen_sprites.draw(self.screen)
        self.map_sprites.draw(self.map_surface)

        self.screen.blit(self.map_surface, (0, self.status_bar_size))
        return

    def update(self):
        if len(self.to_spawn) > 0:
            self.frame += 1
            if self.frame == self.spawn_delay:
                self.enemies.append(self.to_spawn[0])
                self.to_spawn.pop(0)
                self.frame = 0

        for tower in self.towers:
            tower.update()
            target = tower.find_target(self.enemies)
            if target is not None and tower.should_fire():
                self.bullets.append(Bullet(target, tower.position, tower.damage, tower.effect))

        for bullet in self.bullets:
            bullet.seek()
            if bullet.has_hit():
                bullet.target.damage(bullet.damage)
                bullet.target.apply_effect(bullet.effect)
                self.money += bullet.damage
                bullet.exists = False

        # If the wave was defeated, prepare a new spawn
        if len(self.enemies) <= 0:
            self.difficulty += 1
            self.generate_wave()

        self.status_bar.set_money(self.money)
        self.circle_menu.set_money(self.money)
        self.upgrade_menu.set_money(self.money)
        self.screen_sprites.update()
        self.map_sprites.update()
        return

    def clean(self):
        if not self.circle_menu.is_open:
            self.circle_menu.kill()

        if not self.upgrade_menu.is_open:
            self.upgrade_menu.kill()

        for i in range(len(self.enemies) - 1, -1, -1):
            # If the entity was not killed and got to the end
            if not self.enemies[i].exists and self.enemies[i].money > 0\
                    and self.enemies[i].current_square >= len(self.enemies[i].path):
                # Remove popular support
                self.popular_support -= 10
                self.status_bar.set_support(self.popular_support)
                self.enemies[i].kill()
                self.enemies.pop(i)
            # Else if the enemy died
            elif not self.enemies[i].exists and self.enemies[i].money <= 0:
                # Add its money
                self.money += self.money_per_difficulty * self.enemies[i].difficulty
                self.enemies[i].kill()
                self.enemies.pop(i)
            # If we have to despawn for some reason
            elif not self.enemies[i].exists:
                self.enemies[i].kill()
                self.enemies.pop(i)

        for i in range(len(self.bullets) - 1, -1, -1):
            if not self.bullets[i].exists:
                self.bullets[i].kill()
                self.bullets.pop(i)
        return

    def end_game(self):
        self.is_running = False
        return

    def build_tower(self, tower_type):
        square = self.circle_menu.saved_square

        # Don't build on anything but paths
        if square["type"] != types["path"]:
            return

        # If we don't have enough money, return
        if self.money < tower_type["cost"]:
            return

        # Pay the cost
        self.money -= tower_type["cost"]

        # Change the square
        square["type"] = tower_type["type"]
        square["next"].clear()

        # Add the tower itself
        if tower_type["type"] == types["souvenir_shop"]:
            self.towers.append(SouvenirShop(square["position"], self.map_entity.square_size))
        elif tower_type["type"] == types["clothes_shop"]:
            self.towers.append(ClothingShop(square["position"], self.map_entity.square_size))
        elif tower_type["type"] == types["food_shop"]:
            self.towers.append(FoodShop(square["position"], self.map_entity.square_size))

        # Rebuild the map to fit the path
        previous_pos = square["previous"][0]
        previous = self.grid[previous_pos[1]][previous_pos[0]]
        previous["next"].remove(square["position"])
        side = -1 if previous["position"][0] <= self.map_size // 2 else 1

        current = self.grid[previous["position"][1]][previous["position"][0] + side]
        i = 1

        # Make sure we are not working on a shop or current path
        if current["type"] != types["grass"]:
            # Try the side above, under or on the other side
            if self.grid[previous["position"][1]][previous["position"][0] - side]["type"] == types["grass"]:
                current = self.grid[previous["position"][1]][previous["position"][0] - side]
                side = -side
            elif self.grid[previous["position"][1] + 1][previous["position"][0]]["type"] == types["grass"]:
                current = self.grid[previous["position"][1] + 1][previous["position"][0]]
                i = 0
            elif self.grid[previous["position"][1] - 1][previous["position"][0]]["type"] == types["grass"]:
                current = self.grid[previous["position"][1] - 1][previous["position"][0]]
                i = 0

        while i <= self.rebuild_distance and 0 < current["position"][0] + side < self.map_size:
            previous["next"].append(current["position"])
            current["type"] = types["path"]
            current["previous"].append(previous["position"])
            previous = current
            current = self.grid[current["position"][1]][current["position"][0] + side]
            i += 1

        # Go up by the same amount we went to the side
        current = self.grid[previous["position"][1] - 1][previous["position"][0]]
        i = 1
        while i <= self.rebuild_distance and 0 < current["position"][1] - 1 < self.map_size:
            previous["next"].append(current["position"])
            current["type"] = types["path"]
            current["previous"].append(previous["position"])
            previous = current
            current = self.grid[current["position"][1] - 1][current["position"][0]]
            i += 1

        # Go back in reverse to find the path
        current = self.grid[previous["position"][1]][previous["position"][0] - side]
        while current["type"] != types["path"]:
            previous["next"].append(current["position"])
            current["type"] = types["path"]
            current["previous"].append(previous["position"])
            previous = current
            current = self.grid[current["position"][1]][current["position"][0] - side]

        # Finally, connect the path back
        previous["next"].append(current["position"])
        current["previous"].append(previous["position"])

        # Clean the next squares' previous to make sure they aren't connected to the tower
        for next_square_pos in square["next"]:
            next_square = self.grid[next_square_pos[1]][next_square_pos[0]]
            next_square["previous"].remove(square["position"])

        # Update entities
        self.map_entity.set_map(self.grid)
        self.decide_enemies_path()
        for enemy in self.enemies:
            enemy.set_path(self.enemies_path)
        return

    def upgrade_tower(self):
        square = self.upgrade_menu.saved_square

        # Find the tower to update
        for tower in self.towers:
            if tower.grid_position == square["position"]:
                # pay the cost
                self.money -= tower.tower_type["upgrade_cost"] * tower.level
                # upgrade
                tower.upgrade()
                return
        return
