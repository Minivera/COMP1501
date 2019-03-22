from classes.Challenge import Challenge
from classes.Constants import command_results, state_changers


class Scene:
    state_description = "description"
    state_challenge = "challenge"

    def __init__(self, scene):
        self.scene = scene
        self.challenge = None
        if "challenge" in scene:
            self.challenge = Challenge(scene["challenge"])
        self.state = self.state_description

    def describe(self):
        # Check if we're currently in challenge mode
        if self.state == self.state_challenge and self.challenge is not None:
            self.challenge.describe()
            return

        # Otherwise, print the scene description
        print(self.scene["description"])
        return

    def request_commands(self):
        # Check if we're currently in challenge mode
        if self.state == self.state_challenge and self.challenge is not None:
            return self.challenge.request_commands()

        # If the scene is set to auto_run a command
        if "auto_command" in self.scene:
            return self.process_command(self.scene["auto_command"])

        while True:
            action = input("What do you want to do?\n").lower()
            # Loop within the commands
            for command in self.scene["commands"]:
                # If the current action is that command
                if action.startswith(command["command"]) and action.find(command["keyword"]) > -1:
                    return self.process_command(command)

            print("Unknown action\n")

    def process_command(self, command):
        # For challenge actions
        if command["result"]["type"] == command_results["TRIGGER_CHALLENGE"]:
            self.state = self.state_challenge
            return state_changers["CONTINUE"], None

        # For describe actions
        if command["result"]["type"] == command_results["DESCRIBE"]:
            print(command["result"]["description"])
            return state_changers["CONTINUE"], None

        # For lose actions actions
        if command["result"]["type"] == command_results["LOSE"]:
            return state_changers["LOSE"], None

        # For scene change actions
        if command["result"]["type"] == command_results["SWITCH_SCENE"]:
            return state_changers["TO_SCENE"], command["result"]["scene_label"]

        return state_changers["CONTINUE"], None
