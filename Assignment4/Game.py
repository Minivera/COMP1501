from classes.Scene import Scene
from classes.Constants import state_changers


class Game:
    STATE_NONE = -1
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_LOST = 2

    def __init__(self, scenes):
        self.is_running = False
        self.state = self.STATE_NONE
        self.scenes = scenes
        self.current_scene = Scene(scenes[0])

    def start(self):
        self.state = self.STATE_GAME
        self.is_running = True
        return

    def execute(self):
        if self.state == self.STATE_MENU:
            self.execute_menu()
        elif self.state == self.STATE_GAME:
            self.execute_game()
        elif self.state == self.STATE_LOST:
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
        (changer, value) = self.current_scene.request_commands()

        # Execute the state change
        if changer == state_changers["TO_SCENE"]:
            for scene in self.scenes:
                if scene["label"] == value:
                    self.current_scene = Scene(scene)
                    return

        if changer == state_changers["LOSE"]:
            # TODO: Improve this message
            print("You lose\n")
            self.state = self.STATE_LOST

        return
