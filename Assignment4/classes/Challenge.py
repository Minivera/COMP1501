import random
from classes.Constants import state_changers


class Challenge:
    state_attack = "attack"
    state_defence = "defence"

    def __init__(self, challenge):
        self.challenge = challenge
        self.character_die_rolls = []
        self.challenge_die_rolls = []
        self.state = self.state_attack
        self.chosen_die = None
        self.challenge_hp = self.challenge["target_number"]
        self.generate_rolls()

    def generate_rolls(self):
        # Generate the player's die rolls
        if len(self.character_die_rolls) <= 0:
            for i in range(0, 5):
                # TODO: replace 5 with character stat
                # TODO: Add character modifier
                self.character_die_rolls.append(random.randint(1, 6))

        # Generate the challenge's die rolls
        if len(self.challenge_die_rolls) <= 0:
            for i in range(0, self.challenge["difficulty"]):
                self.challenge_die_rolls.append(random.randint(1, 6) + self.challenge["diff_modifier"])

        return

    def describe(self):
        # Print the challenge description
        print(self.challenge["description"])

        # Print the challenge difficulty and stat
        # TODO: Replace with character's stats
        print("This is a challenge based on your {} of {} modified by your {} of {}\n".format(
            self.challenge["stat"],
            5,
            self.challenge["modifier"],
            0,
        ))
        print("The challenge is rolling {} dice with a modifier of {}\n".format(
            self.challenge["difficulty"],
            self.challenge["diff_modifier"],
        ))
        print("The Challenge's difficulty is {}\n".format(
            self.challenge["target_number"],
        ))

        # Print the current state and challenge chosen die
        self.chosen_die = self.challenge_die_rolls.pop()
        if self.state == self.state_attack:
            # TODO: Change the text based on the challenge type
            print("You're on the offensive! Attack against a roll of {}\n".format(self.chosen_die))
        elif self.state == self.state_defence:
            print("You're on the defensive! Defend against a roll of {}\n".format(self.chosen_die))
        return

    def request_commands(self):
        # Print the available dice
        print("You have the dice [{}] at your disposal".format(self.character_die_rolls))

        while True:
            die = int(input("Chose your die\n"))
            if die in self.character_die_rolls:
                self.character_die_rolls.remove(die)
                if die >= self.chosen_die:
                    self.challenge_hp -= die - self.chosen_die
                    print("You win!\n")
                    # TODO: Print a better description based on challenge type
                else:
                    # TODO: Have the character lose some HP
                    print("You lose!\n")
                break
            print("Invalid die chosen\n")

        # Check if the character won
        if self.challenge_hp <= 0:
            print("You have won the challenge!\n")
            return state_changers["TO_SCENE"], self.challenge["won_scene"]
        # TODO: Add the character lose state

        # If either the challenge or the character is missing dice
        if len(self.character_die_rolls) <= 0:
            print("You are out of dice, rerolling\n")
        if len(self.challenge_die_rolls) <= 0:
            print("The challenge is out of dice, rerolling\n")

        # Print the challenge current HP
        print("You still need to remove {} from the target number".format(self.challenge_hp))

        # Continue the challenge
        self.generate_rolls()
        self.state = self.state_defence if self.state == self.state_attack else self.state_attack

        return state_changers["CONTINUE"], None
