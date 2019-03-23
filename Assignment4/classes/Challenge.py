import random
from classes.Constants import state_changers
from helper.ChallengeResultMessages import attack_win_message, attack_lose_message,\
    defence_win_message, defence_lose_message
from helper.ChallengeMessages import attack_message, defence_message


class Challenge:
    state_attack = "attack"
    state_defence = "defence"

    def __init__(self, challenge, character):
        self.challenge = challenge
        self.described = False
        self.character_die_rolls = []
        self.challenge_die_rolls = []
        self.state = self.state_attack
        self.chosen_die = None
        self.challenge_hp = self.challenge["target_number"]
        self.character = character
        self.generate_rolls()

    def generate_rolls(self):
        # Generate the player's die rolls
        if len(self.character_die_rolls) <= 0:
            for i in range(0, self.character.get_stat(self.challenge["stat"])):
                self.character_die_rolls.append(
                    random.randint(1, 6) + self.character.get_modifier(self.challenge["modifier"])
                )

        # Generate the challenge's die rolls
        if len(self.challenge_die_rolls) <= 0:
            for i in range(0, self.challenge["difficulty"]):
                self.challenge_die_rolls.append(random.randint(1, 6) + self.challenge["diff_modifier"])

        return

    def describe(self):
        if not self.described:
            # Print the challenge description
            print(self.challenge["description"])

            # Print the challenge difficulty and stat
            print("This is a challenge based on your {} of {} modified by your {} of +{}\n".format(
                self.challenge["stat"],
                self.character.get_stat(self.challenge["stat"]),
                self.challenge["modifier"],
                self.character.get_modifier(self.challenge["modifier"]),
            ))
            print("The challenge is rolling {} dice with a modifier of +{}\n".format(
                self.challenge["difficulty"],
                self.challenge["diff_modifier"],
            ))
            print("The Challenge's difficulty is {}\n".format(
                self.challenge["target_number"],
            ))
            self.described = True

        # Print the current state and challenge chosen die
        self.chosen_die = self.challenge_die_rolls.pop()
        if self.state == self.state_attack:
            print(attack_message(self.challenge["type"], self.challenge["target"], self.chosen_die))
        elif self.state == self.state_defence:
            print(defence_message(self.challenge["type"], self.challenge["target"], self.chosen_die))
        return

    def request_commands(self):
        # Print the available dice
        print("You have the dice {} at your disposal".format(self.character_die_rolls))

        while True:
            die = int(input("Chose your die\n"))
            if die in self.character_die_rolls:
                self.character_die_rolls.remove(die)
                if self.state == self.state_attack:
                    if die > self.chosen_die:
                        self.challenge_hp -= die - self.chosen_die
                        print(attack_win_message(
                            self.challenge["type"],
                            self.challenge["target"],
                            die - self.chosen_die,
                        ))
                    else:
                        print(attack_lose_message(self.challenge["type"]))
                else:
                    if die >= self.chosen_die:
                        print(defence_win_message(self.challenge["type"]))
                    else:
                        print(defence_lose_message(
                            self.challenge["type"],
                            self.challenge["target"],
                            self.chosen_die - die,
                        ))
                        self.character.health -= self.chosen_die - die
                break
            print("Invalid die chosen\n")

        # Check if the character won
        if self.challenge_hp <= 0:
            print("You have won the challenge!\n")
            return state_changers["TO_SCENE"], self.challenge["won_scene"], False

        if self.character.health <= 0 and "lose_scene" in self.challenge:
            return state_changers["TO_SCENE"], self.challenge["lose_scene"], False
        elif self.character.health <= 0:
            return state_changers["LOSE"], None, False

        # If either the challenge or the character is missing dice
        if len(self.character_die_rolls) <= 0:
            print("You are out of dice, rerolling\n")
        if len(self.challenge_die_rolls) <= 0:
            print("The challenge is out of dice, rerolling\n")

        # Print the challenge current HP
        print("You still need to remove {} from the target number to win\n".format(self.challenge_hp))

        # Continue the challenge
        self.generate_rolls()
        self.state = self.state_defence if self.state == self.state_attack else self.state_attack

        return state_changers["CONTINUE"], None, False
