import random
from classes.Constants import challenge_types

combat_attack_messages = [
    "You're on the offensive, {} defends {}!\n"
]

magical_attack_messages = [
    "It's your turn to use your powers, {} dodges {}!\n"
]

ability_attack_messages = [
    "You are ready to overcome {}, the difficulty is {}\n"
]

social_attack_messages = [
    "You take control of the discussion, attack against {}\n"
]

combat_defence_messages = [
    "You're on the defensive, {} attacks with {}\n"
]

magical_defence_messages = [
    "{} send a power your way, defend with {}\n"
]

ability_defence_messages = [
    "You have to evade {}, you need to beat {}\n"
]

social_defence_messages = [
    "{} moves against you in the discussion, defend against {}"
]


def attack_message(challenge_type, target, roll):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_attack_messages[random.randint(0, len(combat_attack_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_attack_messages[random.randint(0, len(magical_attack_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["ABILITY"]:
        return ability_attack_messages[random.randint(0, len(ability_attack_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["SOCIAL"]:
        return social_attack_messages[random.randint(0, len(social_attack_messages) - 1)].format(target, roll)

    return ""


def defence_message(challenge_type, target, roll):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_defence_messages[random.randint(0, len(combat_defence_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_defence_messages[random.randint(0, len(magical_defence_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["ABILITY"]:
        return ability_defence_messages[random.randint(0, len(ability_defence_messages) - 1)].format(target, roll)
    if challenge_type == challenge_types["SOCIAL"]:
        return social_defence_messages[random.randint(0, len(social_defence_messages) - 1)].format(target, roll)

    return ""
