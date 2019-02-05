import pygame
import random
import game.States
from states.State import State
from game.objects.Unit import Unit

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class MenuState(State):
    def __init__(self):
        self.title = {
            "name": "Awkward dungeons",
            "position": (512, 100),
        }
        self.menus = [
            {
                "name": "Start",
                "label": "start",
                "position": (512, 200),
                "instance": 0,
                "is_clicked": False,
            },
            {
                "name": "Instructions",
                "label": "tutorial",
                "position": (512, 250),
                "instance": 0,
                "is_clicked": False,
            },
            {
                "name": "Quit Game",
                "label": "exit",
                "position": (512, 300),
                "instance": 0,
                "is_clicked": False,
            },
        ]
        self.scenarios = [
            {
                "entities": [
                    Unit("thief", "", 1, (0, 0), 1, (1034, 512)),
                    Unit("orc", "", 1, (0, 0), 1, (1100, 512)),
                ],
                "direction": (-50, 512),
            },
            {
                "entities": [
                    Unit("knight", "", 0, (0, 0), 1, (-100, 512)),
                    Unit("goblin", "", 0, (0, 0), 1, (-50, 512)),
                ],
                "direction": (1034, 512),
            }
        ]
        self.current_scenario = self.scenarios[random.randint(0, len(self.scenarios) - 1)]
        self.title_font = pygame.font.Font("assets/fonts/AwkwardExt.ttf", 64)
        self.main_font = pygame.font.Font("assets/fonts/Awkward.ttf", 52)
        self.next_state = False
        self.__initialize()

    def __initialize(self):
        title_font = self.title_font.render(self.title["name"], True, WHITE)
        self.title["position"] = (
            self.title["position"][0] - title_font.get_width() // 2,
            self.title["position"][1] - title_font.get_height() // 2
        )
        self.title["instance"] = title_font

        for menu in self.menus:
            rendered_font = self.main_font.render(menu["name"], True, WHITE)
            menu["position"] = (
                menu["position"][0] - rendered_font.get_width() // 2,
                menu["position"][1] - rendered_font.get_height() // 2
            )
            menu["instance"] = rendered_font

        for unit in self.current_scenario["entities"]:
            unit.run_to(self.current_scenario["direction"])
        return

    def handle_input(self, game_instance):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_instance.end_game()
                return

            if event.type == pygame.MOUSEBUTTONUP:
                self.handle_mouse_click()
        return

    def render(self, game_instance, sprites):
        # Ignore if leaving state
        if self.next_state:
            return

        game_instance.screen.fill(BLACK)

        game_instance.screen.blit(self.title["instance"], self.title["position"])
        for menu in self.menus:
            game_instance.screen.blit(menu["instance"], menu["position"])

        for unit in self.current_scenario["entities"]:
            sprites.add(unit.entity)
            sprites.add(unit.emote_entity)
        return

    def update(self, game_instance):
        # Ignore if leaving state
        if self.next_state:
            return

        for unit in self.current_scenario["entities"]:
            unit.update()

        for menu in self.menus:
            if menu["is_clicked"] and menu["label"] == "start":
                self.next_state = game.States.STATE_GAME
                return
            if menu["is_clicked"] and menu["label"] == "tutorial":
                self.next_state = game.States.STATE_TUTORIAL
                return
            if menu["is_clicked"] and menu["label"] == "exit":
                game_instance.end_game()
                return

        return

    def clean(self, game_instance):
        if self.next_state:
            for unit in self.current_scenario["entities"]:
                unit.clean()
            game_instance.change_state(self.next_state)
            return

        # Check if the menu scenario is finished
        ended = True
        for unit in self.current_scenario["entities"]:
            if not unit.move_finished():
                ended = False

        # If finished, assign a new one
        if ended:
            for unit in self.current_scenario["entities"]:
                unit.clean()
            self.current_scenario = self.scenarios[random.randint(0, len(self.scenarios) - 1)]
            for unit in self.current_scenario["entities"]:
                unit.reset_position()
                unit.run_to(self.current_scenario["direction"])
        return

    def handle_mouse_click(self):
        mouse = pygame.mouse.get_pos()
        for menu in self.menus:
            menu_rect = pygame.Rect(menu["position"], (menu["instance"].get_width(), menu["instance"].get_height()))
            if menu_rect.collidepoint(mouse[0], mouse[1]):
                menu["is_clicked"] = True
        return
