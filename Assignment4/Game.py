from classes.Scene import Scene
from classes.Character import Character
from classes.Constants import state_changers, stats, modifiers


class Game:
    STATE_NONE = -1
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_LOST = 2
    STATE_WON = 3

    base_health = 5

    total_objectives = 10

    def __init__(self, scenes):
        self.is_running = False
        self.state = self.STATE_NONE
        self.objectives_completed = 0
        # TODO: Have a real character creation
        self.character = Character("test")
        self.character.set_stat(stats["BODY"], 4)
        self.character.set_stat(stats["MIND"], 6)
        self.character.set_stat(stats["SOUL"], 3)
        self.character.set_modifier(modifiers["SKILL"], 1)
        self.character.set_modifier(modifiers["POWER"], 2)
        self.character.set_modifier(modifiers["CHARISMA"], 1)
        self.character.health = self.base_health * self.character.get_stat(stats["BODY"])
        self.scenes = scenes
        self.current_scene = Scene(scenes[0], self.character)

    def start(self):
        self.state = self.STATE_GAME
        self.is_running = True
        return

    def execute(self):
        if self.state == self.STATE_MENU:
            self.execute_menu()
        elif self.state == self.STATE_GAME:
            self.execute_game()
        elif self.state == self.STATE_LOST or self.state == self.STATE_WON:
            self.execute_lost()
        return

    def execute_menu(self):
        return

    def execute_lost(self):
        self.is_running = False
        return

    def execute_game(self):
        # Describe the current scene
        self.current_scene.describe()

        # Process the commands for that scene
        (changer, value, objective_scene) = self.current_scene.request_commands()

        # Execute the state change
        if changer == state_changers["TO_SCENE"]:
            for scene in self.scenes:
                if scene["label"] == value:
                    self.current_scene = Scene(scene, self.character)
        elif changer == state_changers["LOSE"]:
            # TODO: Improve this message
            print("You lose\n")
            self.state = self.STATE_LOST

        if objective_scene and self.objectives_completed < self.total_objectives - 1:
            self.objectives_completed += 1
            print("You have successfully completed an objective! {} to go \n".format(
                self.total_objectives - self.objectives_completed
            ))
        elif objective_scene and self.objectives_completed < self.total_objectives - 1:
            self.objectives_completed += 1
            print("You have completed all {} objectives. Congratulations!".format(self.objectives_completed))
            self.state = self.STATE_WON

        return
