import copy
from classes.Challenge import Challenge
from constants.Constants import command_results, state_changers


class Scene:
    state_description = "description"
    state_challenge = "challenge"

    def __init__(self, scene, character, ran_commands, saved_values):
        self.scene = copy.deepcopy(scene)
        self.character = character
        self.challenge = None
        self.ran_commands = ran_commands
        self.saved_values = saved_values
        if "challenge" in scene:
            self.challenge = Challenge(scene["challenge"], character)
        self.state = self.state_description

    def describe(self):
        # Check if we're currently in challenge mode
        if self.state == self.state_challenge and self.challenge is not None:
            self.challenge.describe()
            return

        # Otherwise, print the scene description
        if isinstance(self.scene["description"], list):
            for description in self.scene["description"]:
                print(description)
                input("Press any key to continue...\n")
        else:
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
            # check if we want to see the character sheet
            if action.startswith("see") and action.find("character") > -1:
                return self.process_command({
                    "command": "see",
                    "keyword": "character",
                    "result": {
                      "type": "describe",
                      "description": self.character.get_description(),
                    }
                })

            # Loop within the commands
            for command in self.scene["commands"]:
                # If the current action is that command
                if action.startswith(command["command"]) and action.find(command["keyword"]) > -1:
                    return self.process_command(command)

            print("Unknown action\n")

    def process_command(self, command):
        command_result = command["result"]
        changer = state_changers["CONTINUE"]
        values = None
        is_objective = False

        # Check if that command was already run and we have another command to run
        if "command" in command and "{}_{}_{}".format(self.scene["label"], command["command"], command["keyword"])\
                in self.ran_commands and "replay_result" in command:
            # change the command result for the replay command
            command_result = command["replay_result"]

        if "if" in command:
            if command["if"]["key"] in self.saved_values and\
                    command["if"]["value"] == self.saved_values[command["if"]["key"]]:
                command_result = command["if"]["result"]

        # For challenge actions
        if command_result["type"] == command_results["TRIGGER_CHALLENGE"]:
            self.state = self.state_challenge
            changer = state_changers["CONTINUE"]
            values = {
                "command": command,
            }
            is_objective = False

        # For describe actions
        elif command_result["type"] == command_results["DESCRIBE"]:
            if isinstance(command_result["description"], list):
                for description in command_result["description"]:
                    print(description)
                    input("Press any key to continue...\n")
            else:
                print(command_result["description"])

            changer = state_changers["CONTINUE"]
            values = {
                "command": command,
            }
            is_objective = False

        # For add stat action actions
        elif command_result["type"] == command_results["INCREASE_STAT"]:
            print(command_result["description"])

            changer = state_changers["INCREASE_STAT"]
            values = {
                "stat": command_result["stat"],
                "amount": command_result["increase"],
                "command": command,
            }
            is_objective = False

        # For describe actions
        elif command_result["type"] == command_results["ADD_TOOL"]:
            print(command_result["description"])

            changer = state_changers["ADD_TOOL"]
            values = {
                "tool": command_result["tool"],
                "command": command,
            }
            is_objective = False

        # For switch scene and increase stat actions
        elif command_result["type"] == command_results["INCREASE_STAT_AND_SWITCH"]:
            print(command_result["description"])

            changer = state_changers["INCREASE_STAT_AND_SWITCH"]
            values = {
                "stat": command_result["stat"],
                "amount": command_result["increase"],
                "new_label": command_result["scene_label"],
                "command": command,
            }
            is_objective = False

        # For switch scene and add tool actions
        elif command_result["type"] == command_results["ADD_TOOL_AND_SWITCH"]:
            print(command_result["description"])

            changer = state_changers["ADD_TOOL_AND_SWITCH"]
            values = {
                "tool": command_result["tool"],
                "new_label": command_result["scene_label"],
                "command": command,
            }
            is_objective = False

        # For switch scene and add tool/stat actions
        elif command_result["type"] == command_results["ADD_TOOL_AND_STAT_AND_SWITCH"]:
            print(command_result["description"])

            changer = state_changers["ADD_TOOL_AND_STAT_AND_SWITCH"]
            values = {
                "stat": command_result["stat"],
                "amount": command_result["increase"],
                "tool": command_result["tool"],
                "new_label": command_result["scene_label"],
                "command": command,
            }
            is_objective = False

        # For lose actions actions
        elif command_result["type"] == command_results["LOSE"]:
            changer = state_changers["LOSE"]
            values = {
                "command": command,
            }
            is_objective = False

        # For scene change actions
        elif command_result["type"] == command_results["SWITCH_SCENE"]:
            changer = state_changers["TO_SCENE"]
            values = {
                "command": command,
                "new_label": command_result["scene_label"],
            }
            is_objective = "is_objective" in self.scene and self.scene["is_objective"]

        # For the end game action
        elif command_result["type"] == command_results["END"]:
            changer = state_changers["END"]
            values = {
                "command": command,
            }
            is_objective = "is_objective" in self.scene and self.scene["is_objective"]

        if "save" in command_result:
            values["save"] = command_result["save"]

        return changer, values, is_objective
