import copy
from classes.Challenge import Challenge
from classes.Constants import command_results, state_changers


class Scene:
    state_description = "description"
    state_challenge = "challenge"

    def __init__(self, scene, character):
        self.scene = copy.deepcopy(scene)
        self.challenge = None
        if "challenge" in scene:
            self.challenge = Challenge(scene["challenge"], character)
        self.state = self.state_description
        if "auto_command" not in self.scene:
            # If no auto command, add a command to see the character status
            self.scene["commands"].append({
                "command": "see",
                "keyword": "character",
                "result": {
                  "type": "describe",
                  "description": character.get_description(),
                }
            })

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
            (next_state, info, is_objective) = self.challenge.request_commands()
            # If changing scene, make sure this scene was marked as an objective
            if next_state == state_changers["TO_SCENE"]:
                return next_state, info, "is_objective" in self.scene and self.scene["is_objective"]
            # Otherwise, return as is
            return next_state, info, is_objective

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
            return state_changers["CONTINUE"], None, False

        # For describe actions
        if command["result"]["type"] == command_results["DESCRIBE"]:
            print(command["result"]["description"])
            return state_changers["CONTINUE"], None, False

        # For lose actions actions
        if command["result"]["type"] == command_results["LOSE"]:
            return state_changers["LOSE"], None, False

        # For scene change actions
        if command["result"]["type"] == command_results["SWITCH_SCENE"]:
            return state_changers["TO_SCENE"], command["result"]["scene_label"],\
                   "is_objective" in self.scene and self.scene["is_objective"]

        return state_changers["CONTINUE"], None, False
