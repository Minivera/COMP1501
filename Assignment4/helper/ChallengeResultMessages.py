import random
from classes.Constants import challenge_types

combat_attack_win_messages = [
    "BAM! You successfully damaged {}, you cause {} damage\n"
]

magical_attack_win_messages = [
    "FWOUSH! You successfully used your powers against {}, you cause {} damage\n"
]

ability_attack_win_messages = [
    "WOW! You successfully worked towards overcoming {}, you reduce the target by {}\n"
]

social_attack_win_messages = [
    "...whisper... You successfully woowed {}, you reduce the target by {}\n"
]

combat_attack_lose_messages = [
    "MISS!\n"
]

magical_attack_lose_messages = [
    "BOOM! The power misses\n"
]

ability_attack_lose_messages = [
    "Failed! Don't overexert yourself!\n"
]

social_attack_lose_messages = [
    "What did you say? That's a failure\n"
]

combat_defence_win_messages = [
    "CLANG! You successfully defended against the attack\n"
]

magical_defence_win_messages = [
    "DODGE! You successfully defended against the attack\n"
]

ability_defence_win_messages = [
    "OUF! You successfully avoided the hazard\n"
]

social_defence_win_messages = [
    "GASP! You successfully avoided the trap laid in front of you\n"
]

combat_defence_lose_messages = [
    "OUCH! You could not avoid the attack from {} and lost {} HP\n"
]

magical_defence_lose_messages = [
    "KABOOM! You could not avoid the power from {} and lost {} HP\n"
]

ability_defence_lose_messages = [
    "Failed! You slipped after trying to survive {} and lost {} HP\n"
]

social_defence_lose_messages = [
    "Oh no! You fell into {}'s trap and lost {} HP\n"
]


def attack_win_message(challenge_type, target, damage):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_attack_win_messages[random.randint(0, len(combat_attack_win_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_attack_win_messages[random.randint(0, len(magical_attack_win_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["ABILITY"]:
        return ability_attack_win_messages[random.randint(0, len(ability_attack_win_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["SOCIAL"]:
        return social_attack_win_messages[random.randint(0, len(social_attack_win_messages) - 1)]\
            .format(target, damage)

    return ""


def attack_lose_message(challenge_type):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_attack_lose_messages[random.randint(0, len(combat_attack_lose_messages) - 1)]
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_attack_lose_messages[random.randint(0, len(magical_attack_lose_messages) - 1)]
    if challenge_type == challenge_types["ABILITY"]:
        return ability_attack_lose_messages[random.randint(0, len(ability_attack_lose_messages) - 1)]
    if challenge_type == challenge_types["SOCIAL"]:
        return social_attack_lose_messages[random.randint(0, len(social_attack_lose_messages) - 1)]

    return ""


def defence_win_message(challenge_type):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_defence_win_messages[random.randint(0, len(combat_defence_win_messages) - 1)]
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_defence_win_messages[random.randint(0, len(magical_defence_win_messages) - 1)]
    if challenge_type == challenge_types["ABILITY"]:
        return ability_defence_win_messages[random.randint(0, len(ability_defence_win_messages) - 1)]
    if challenge_type == challenge_types["SOCIAL"]:
        return social_defence_win_messages[random.randint(0, len(social_defence_win_messages) - 1)]

    return ""


def defence_lose_message(challenge_type, target, damage):
    if challenge_type == challenge_types["COMBAT"]:
        return combat_defence_lose_messages[random.randint(0, len(combat_defence_lose_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["MAGICAL"]:
        return magical_defence_lose_messages[random.randint(0, len(magical_defence_lose_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["ABILITY"]:
        return ability_defence_lose_messages[random.randint(0, len(ability_defence_lose_messages) - 1)]\
            .format(target, damage)
    if challenge_type == challenge_types["SOCIAL"]:
        return social_defence_lose_messages[random.randint(0, len(social_defence_lose_messages) - 1)]\
            .format(target, damage)

    return ""
