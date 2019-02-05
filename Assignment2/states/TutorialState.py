import pygame
import game.States
from states.State import State
from game.objects.Unit import Unit
from entities.UIBlock import UIBlock
from entities.Text import Text

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class TutorialState(State):
    def __init__(self):
        self.tutorials = []
        self.current_tutorial = 0
        self.change_to_tutorial = False

        self.top_width = 84 * 4
        self.top_height = 44 * 1
        self.top_menu = UIBlock((self.top_width, self.top_height), (512 - self.top_width, 140 - self.top_height * 2))

        self.central_width = 84 * 4
        self.central_height = 44 * 5
        self.central_menu = UIBlock((self.central_width, self.central_height), (512 - self.central_width, 150))

        self.bottom_width = 84 * 4
        self. bottom_height = 44 * 1
        self.bottom_menu = UIBlock(
            (self.bottom_width, self.bottom_height),
            (512 - self.bottom_width, 150 + self.central_height * 2 + 10)
        )

        self.next_state = False
        self.__initialize()

    def __initialize(self):
        self.tutorials = [
            {
                "title": "Welcome to Awkward Dungeons",
                "description": [
                    "Awkward Dungeons is a puzzle game where you will try to guide three",
                    "adventurers through a dungeon without being able to control them directly.",
                    "The adventurers only react depending on their objectives and fears.",
                    "",
                    "",
                    "You will only have control over the objects scattered throughout",
                    "the dungeon. Using a limited amount of moves and the needs of the",
                    "adventurers, your objective is to guide them to the exit."
                ],
                "text": 0,
                "description_entities": [],
                "entities": [
                    Unit("thief", False, 1, (0, 0), 1, (420, 400)),
                    Unit("wizard", "angry", 1, (0, 0), 1, (460, 400)),
                    Unit("knight", False, 1, (0, 0), 1, (500, 400)),
                ],
                "buttons": []
            }
        ]
        self.make_tutorial_sprites()

    def make_tutorial_sprites(self):
        tutorial = self.tutorials[self.current_tutorial]
        tutorial["text"] = Text(52, tutorial["title"], WHITE, (527, 85), (self.top_width * 2, 52), True)
        position = 160
        for description in tutorial["description"]:
            text = Text(
                32,
                description,
                WHITE,
                (512 - self.central_width + 24, position),
                (self.central_width * 2, 24)
            )
            tutorial["description_entities"].append(text)
            position += 21

        if self.current_tutorial > 0:
            tutorial["buttons"].append({
                "label": "previous",
                "instance": Text(
                    40,
                    "Previous",
                    WHITE,
                    (512 - self.central_width + 24, 615),
                    (self.central_width, 32)
                ),
                "is_clicked": False,
            })

        tutorial["buttons"].append({
            "label": "next",
            "instance": Text(
                40,
                "Next" if self.current_tutorial + 1 < len(self.tutorials) else "Menu",
                WHITE,
                (512 + self.central_width - 150, 615),
                (self.central_width, 32)
            ),
            "is_clicked": False,
        })

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
        game_instance.screen.fill(BLACK)

        sprites.add(self.top_menu)
        sprites.add(self.central_menu)
        sprites.add(self.bottom_menu)

        tutorial = self.tutorials[self.current_tutorial]
        sprites.add(tutorial["text"])

        for entity in tutorial["description_entities"]:
            sprites.add(entity)

        for unit in tutorial["entities"]:
            sprites.add(unit.entity)
            sprites.add(unit.emote_entity)

        for entity in tutorial["buttons"]:
            sprites.add(entity["instance"])
        return

    def update(self, game_instance):
        tutorial = self.tutorials[self.current_tutorial]
        for unit in tutorial["entities"]:
            unit.update()

        tutorial = self.tutorials[self.current_tutorial]
        for button in tutorial["buttons"]:
            if button["is_clicked"] and button["label"] == "previous":
                self.current_tutorial -= 1
                return
            if button["is_clicked"] and button["label"] == "next":
                if self.current_tutorial + 1 >= len(self.tutorials):
                    self.next_state = game.States.STATE_MENU
                else:
                    self.current_tutorial += 1
                return
        return

    def clean(self, game_instance):
        if self.next_state:
            self.top_menu.kill()
            self.central_menu.kill()
            self.bottom_menu.kill()

            tutorial = self.tutorials[self.current_tutorial]
            tutorial["text"].kill()

            for entity in tutorial["description_entities"]:
                entity.kill()

            for unit in tutorial["entities"]:
                unit.clean()

            for entity in tutorial["buttons"]:
                entity["instance"].kill()

            game_instance.change_state(self.next_state)
        return

    def handle_mouse_click(self):
        mouse = pygame.mouse.get_pos()
        tutorial = self.tutorials[self.current_tutorial]
        for button in tutorial["buttons"]:
            button_rect = button["instance"].rect
            if button_rect.collidepoint(mouse[0], mouse[1]):
                button["is_clicked"] = True
        return
