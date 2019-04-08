from classes.Scene import Scene
from classes.Character import Character
from constants.Constants import state_changers


class Game:
    STATE_NONE = -1
    STATE_MENU = 0
    STATE_GAME = 1
    STATE_LOST = 2
    STATE_WON = 3

    total_objectives = 10

    def __init__(self, scenes):
        self.is_running = False
        self.state = self.STATE_NONE
        self.objectives_completed = 0
        self.ran_commands = {}
        self.saved_values = {}
        self.character = None
        self.scenes = scenes
        self.current_scene = Scene(scenes[0], self.character, self.ran_commands, self.saved_values)
        # Try to load the "start" scene rather than the first one
        for scene in self.scenes:
            if scene["label"] == "start":
                self.current_scene = Scene(scene, self.character, self.ran_commands, self.saved_values)

    def start(self):
        self.state = self.STATE_MENU
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
        print(
            '"Welcome, thank you for accepting my request for an interview."\n',
            'You: "You\'re not the first who asked about the heist you know, I sure hope you find something',
            'more to say."\n',
            '"Do not worry... To start, can you say your name out loud for the recording?"\n',
        )
        while True:
            name = input("Sure, it's...\n")
            if name == "":
                print('"I didn\'t quite hear what you said, can you repeat?"\n')
            else:
                self.character = Character(name)
                break

        print(
            '"Thank you, now, can you explain how your heist worked exactly?"\n',
            'You: "Yeah, it was pretty simple really, all I had to do was say what I wanted to do and roll dice"\n',
            '"Roll dice?"\n',
            'You: "As I said, roll dice. When I got in front of something difficult or dangerous you see, I had to',
            'roll dice equal to the best stat for the task"\n',
            '"Hm hm"\n',
        )

        input("Press any key to continue...\n")
        print(
            'You: "Then, if I had a tool available, I could add +2 to each dice rolled"\n',
            '"Of course"\n',
            'You: "So, whenever I was asked to challenge myself, I would roll those dice and the challenge would roll',
            'theirs with their own modifier. Now it was a matter of choosing the dice. Every turn, I would attack',
            'and then the challenge would attack back."\n',
            '"That sounds difficult"\n',
        )

        input("Press any key to continue...\n")
        print(
            'You: "It kinda was! So, if I was on the attack, I had to chose a dice that was higher than the',
            'challenge\'s chosen die to hurt them. If I was on the defense, I needed to chose a die equal or higher to',
            'avoid getting hurt."\n',
            '"And what if you succeeded?"\n',
        )

        input("Press any key to continue...\n")
        print(
            'You: "If I succeeded on my attack, I\'d hurt the challenge! On the other hand, if I successfully defended',
            ', I would avoid getting hurt myself."\n',
            '"Hm hm"\n',
            'You: "Then, it was a matter of hurting the challenge enough to lower the target to 0 while avoiding',
            'getting my own health bellow 0, simple right?"\n',
            '"Very specific"\n',
        )

        input("Press any key to continue...\n")
        print(
            'You: "Another great thing was, if I wanted to look at my current status, I could say `see character`',
            'and my status would show up!"\n',
            '"Make sense"\n',
            'You: "It\'s great you understand. Everyone call me crazy."\n',
        )

        input("Press any key to continue...\n")
        print(
            '"Right... So about that heist?"\n',
            'You: "Of course, let me start from the beginning, I was in my loft when I got new of a big haul at',
            'the nearest vault..."\n',
        )
        self.state = self.STATE_GAME
        return

    def execute_lost(self):
        self.is_running = False
        return

    def execute_game(self):
        # Describe the current scene
        self.current_scene.describe()

        # Process the commands for that scene
        (changer, value, objective_scene) = self.current_scene.request_commands()

        # If we are given a command to save and it's not and auto command
        if value is not None and "command" in value and "command" in value["command"]:
            self.ran_commands["{}_{}_{}".format(
                self.current_scene.scene["label"],
                value["command"]["command"],
                value["command"]["keyword"]
            )] = True

        if value is not None and "lower_tool" in value:
            self.character.remove_tool(value["lower_tool"])

        if value is not None and "save" in value:
            self.saved_values[value["save"]] = self.saved_values[value["save"]] + 1 if value["save"] \
                                                                                       in self.saved_values else 1

        # Execute the state change
        # Simple scene changer
        if changer == state_changers["TO_SCENE"]:
            for scene in self.scenes:
                if scene["label"] == value["new_label"]:
                    self.current_scene = Scene(scene, self.character, self.ran_commands, self.saved_values)
        # Increase a stat
        elif changer == state_changers["INCREASE_STAT"]:
            if isinstance(value["stat"], list):
                for val in value["stat"]:
                    self.character.increase_stat(val, value["amount"])
                    print("Increased {} by {}!".format(val, value["amount"]))
            else:
                self.character.increase_stat(value["stat"], value["amount"])
                print("Increased {} by {}!".format(value["stat"], value["amount"]))
        # Add a new tool to inventory
        elif changer == state_changers["ADD_TOOL"]:
            if isinstance(value["tool"], list):
                for val in value["tool"]:
                    self.character.add_tool(val)
                    print("Picked up 1 {}!".format(val))
            else:
                self.character.add_tool(value["tool"])
                print("Picked up 1 {}!".format(value["tool"]))
        # Increase a stat and change scene
        elif changer == state_changers["INCREASE_STAT_AND_SWITCH"]:
            # Start by increasing the stat
            if isinstance(value["stat"], list):
                for val in value["stat"]:
                    self.character.increase_stat(val, value["amount"])
                    print("Increased {} by {}!".format(val, value["amount"]))
            else:
                self.character.increase_stat(value["stat"], value["amount"])
                print("Increased {} by {}!".format(value["stat"], value["amount"]))
            # Then switch scene
            for scene in self.scenes:
                if scene["label"] == value["new_label"]:
                    self.current_scene = Scene(scene, self.character, self.ran_commands, self.saved_values)
        # Add a new tool to inventory and change scene
        elif changer == state_changers["ADD_TOOL_AND_SWITCH"]:
            # Start by adding the tool
            if isinstance(value["tool"], list):
                for val in value["tool"]:
                    self.character.add_tool(val)
                    print("Picked up 1 {}!".format(val))
            else:
                self.character.add_tool(value["tool"])
                print("Picked up 1 {}!".format(value["tool"]))
            # Then switch scene
            for scene in self.scenes:
                if scene["label"] == value["new_label"]:
                    self.current_scene = Scene(scene, self.character, self.ran_commands, self.saved_values)
        # Add a new tool to inventory, increase a stat and change scene
        elif changer == state_changers["ADD_TOOL_AND_STAT_AND_SWITCH"]:
            # Start by adding the tool
            if isinstance(value["tool"], list):
                for val in value["tool"]:
                    self.character.add_tool(val)
                    print("Picked up 1 {}!".format(val))
            else:
                self.character.add_tool(value["tool"])
                print("Picked up 1 {}!".format(value["tool"]))
            # Then increase the stat
            if isinstance(value["stat"], list):
                for val in value["stat"]:
                    self.character.increase_stat(val, value["amount"])
                    print("Increased {} by {}!".format(val, value["amount"]))
            else:
                self.character.increase_stat(value["stat"], value["amount"])
                print("Increased {} by {}!".format(value["stat"], value["amount"]))
            # Then switch scene
            for scene in self.scenes:
                if scene["label"] == value["new_label"]:
                    self.current_scene = Scene(scene, self.character, self.ran_commands, self.saved_values)
        # Lose the game
        elif changer == state_changers["LOSE"]:
            # TODO: Improve this message
            print("You lose\n")
            self.state = self.STATE_LOST
        # End the game
        elif changer == state_changers["END"]:
            print("You finished the game\n")

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
