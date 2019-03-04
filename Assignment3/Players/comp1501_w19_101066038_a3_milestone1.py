# -> 101066038
#
# This is an Ai player for the game glad-AI-tors. This agent is made up to three main states, each containing a sub
# state machine.
#
# The WANDER main state happens when both players, or at least the current player and the last info about the detected
# player, do not have a weapon in the possession. It is also the starting state of the agent.
#
# In wander, the agent will start looking around while moving towards the center to look for a weapon. If it
# detects a player, it will adjust it's behavior according to its current situation. If the detected player has
# a weapon, go to the CAUTIOUS main state. When the agent detects a weapon, it will move towards the weapon's position
# by changing to the get_weapon state and try to obtain it. If the agent obtains a weapon, it will change to the
# AGGRESSIVE main state. At any point, if the agent detects a hazard in the general direction it's going, it will move
# to the evade state. It will return to the previous state once the hazard is evaded.
#
# The CAUTIOUS main state happens when the detected player has a weapon. In that main state, the agent will try to keep
# an eye on the detected player while evading attacks and hiding behind columns.
#
# In wander, the agent will try to move perpendicular to the last known position of the detect player and scan for it.
# If it detects a player, it updates the last known position of that player and tries to hide behind a column. The
# agent will hide behind a column considering the last known position of the detected player and will keep switching
# between the hide state and the peek state. In peek, the agent will scan for the player in the last known position and
# for weapons if it does not own any. It will move away from the column for this scan, but will stay near. If the agent
# detects a weapon in its vicinity and it does not have a weapon, it will move to the get_weapon state and try to get
# it. If the agent ever detects a player, it will check it's status and move to the AGGRESSIVE main state if the agent
# has a weapon and the player does not or to the WANDER main state is both don't have a weapon. At any point, if the
# agent detects a hazard in the general direction it's going, it will move to the evade state. It will return to the
# previous state once the hazard is evaded.
#
# The AGGRESSIVE main state happens when the detected player doesn't have a weapon or the agent has a health advantage
# on the detected player. In that state, the agent will try to get behind the detected player and shoot them.
#
# In the wander state, the agent will scan for a target will moving towards the closest side. If the agent detects a
# player, it will move to the get_behind state to try and shoot it. If the agent is close enough to the target, it will
# move to the fire state where it will make sure the target is still there, calculate a nice angle and shoot the weapon
# it is holding. Once fired, it will move back to the WANDER main state if the shot player does not have a weapon or
# to CAUTIOUS if the player does.  At any point, if the agent detects a hazard in the general direction it's going, it
# will move to the evade state. It will return to the previous state once the hazard is evaded.
#
# The scanning behavior of the agent will first be semi random, trying to look for targets and save them in memory.
# Once the agent has targets saved, it will always scan between the last position and the saved velocity of the target
# to try to keep an eye on them ans save some cycles.
#
# The 8 spots in memory are reserved for the following data
#
# SAVE_A: Last state letter value
# SAVE_B: Target 1 type.
# SAVE_C: Target 1 distance as a two unicode characters (x, y). Convert the char to an int. Offset of 750.
# SAVE_D: Target 1 angle as a single unicode character.
# SAVE_E: Target 2 type.
# SAVE_F: Target 2 distance as a two unicode characters (x, y). Convert the char to an int. Offset of 750.
# SAVE_X: Target 2 angle as a single unicode character.
# SAVE_Y: Reserved

import random
import math

arena_dimensions = (750,  750)

acceptable_distance = 60

small_scan_range = 10

types = {
    "column": "0C",
    "player": "0P",
    "weapon": "0W",
    "hazard": "0H",
    "wall": "0M",
}

reverse_types = {
    "0C": "column",
    "0P": "player",
    "0W": "weapon",
    "0H": "hazard",
    "0M": "wall",
}

states = {
    "wander": "0W",
    "get_weapon": "0G",
    "evade": "0E",
    "hide": "0H",
    "peek": "0P",
    "go_behind": "0B",
    "fire": "0F",
}

reverse_states = {
    "0W": "wander",
    "0G": "get_weapon",
    "0E": "evade",
    "0H": "hide",
    "0P": "peek",
    "0B": "go_behind",
    "0F": "fire",
}


def start():
    """
    Start function that defines the starting state of the agent.
    :return: The wander state of the WANDER main state and an empty dictionary
    """
    return "w_wander", {}


def w_wander():
    """
    The wander state of the WANDER main state, identified by the chars 0A. This state makes the agent move towards the
    center while scanning for targets. It will save the position of the player if any as target 1 and the position of
    the nearest weapon as target 2. it will also keep scanning for where it is going to evade any traps if they get
    too close.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "w_wander"

    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info, target2_type,
        target2_distance, target2_angle, target2_info) = scan_for_targets(values, "player", "weapon")

    # If a weapon is in view and we don,t have a weapon, change state to go grab it
    #if target2_type == "weapon" and get_if_have_weapon():
    #    next_state = "w_get_weapon"

    # Accelerate towards the middle
    steps_number = max(abs(arena_dimensions[0] / 2 - position[0]), abs(arena_dimensions[1] / 2 - position[1]))

    dx = float(arena_dimensions[0] / 2 - position[0]) / steps_number
    dy = float(arena_dimensions[1] / 2 - position[1]) / steps_number

    # If we found a player, turn to face it
    rot_cc = 0
    rot_cw = 0
    if target1_type == types["player"]:
        # Get current angle and compare it with the desired angle
        throw = get_throwing_angle()
        delta = ((target1_angle - throw) + 360) % 360

        if delta > 180:
            rot_cc = 0
            rot_cw = 1
        else:
            rot_cc = 1
            rot_cw = 0

    # Make sure we evade anything we're moving towards
    (danger, danger_type, danger_distance, danger_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "w_evade"
        target2_type = danger_type
        target2_distance = danger_distance
        target2_angle = danger_angle


    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle)


def w_get_weapon():
    return "", {}


def w_evade():
    """
    The evade state of the WANDER main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return:  The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("w_", "player", "weapon")


def c_wander():
    return "", {}


def c_hide():
    return "", {}


def c_peek():
    return "", {}


def c_get_weapon():
    return "", {}


def c_evade():
    return "", {}


def a_wander():
    return "", {}


def a_go_behind():
    return "", {}


def a_fire():
    return "", {}


def a_evade():
    return "", {}


def shared_get_weapon(main_state, main_target):
    """
    This shared get_weapon code allows the multiple get_weapon state to share their code. This code will look for the
    weapon and propose a move towards it. It will relay the main target as a secondary target while it looks for the
    weapon.
    :return: The next state and a dictionary of information to send back to the game.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = main_state + "get_weapon"

    # Scan for a weapon and optionally the other target
    (_, _, _, _, weapon_type, weapon_distance, weapon_angle, weapon_info) = \
        scan_for_targets(values, main_target, "weapon")

    # If the weapon is dangerous
    if weapon_info:
        # Try a secondary scan with empty values
        new_values = [
            values[0],
            values[1],
            values[2],
            values[3],
            "\x00\x00",
            "\x00\x00",
            "\x00\x00",
            values[7],
        ]

        (_, _, _, _, weapon_type, weapon_distance, weapon_angle, weapon_info) = \
            scan_for_targets(new_values, main_target, "weapon")

    # If the weapon is still dangerous
    if weapon_info:
        # Return to the previous state


def shared_evade(main_state, primary_target, secondary_target):
    """
    This shared evade code allows the multiple evade states to hare their base code. Evade makes the agent flee
    the nearest hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = main_state + "evade"

    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, _, _, _, _, _) = \
        scan_for_targets(values, primary_target, secondary_target)

    danger_type = "\x00\x00"
    danger_angle = 0

    # Check if we have a targeted hazard
    if values[4] != "\x00\x00" and values[5] != "\x00\x00" and values[6] != "\x00\x00":
        danger_type = values[4]
        danger_angle = ord(values[6][:1])

    dx = 0
    dy = 0
    # Accelerate away from danger if any is saved
    if danger_type != "\x00\x00":
        target_angle = danger_angle - 180
        if target_angle < 0:
            target_angle += 359

        target = vector_to_components(10, target_angle)
        steps_number = max(abs(target[0] / 2 - position[0]), abs(target[1] / 2 - position[1]))

        dx = float(target[0] / 2 - position[0]) / steps_number
        dy = float(target[1] / 2 - position[1]) / steps_number

    # Make sure we evade anything we're moving towards
    (danger, danger_type, danger_distance, danger_angle) = scan_for_danger(position, get_velocity_tuple())
    if not danger:
        next_state = main_state + reverse_states[values[0]]

    return next_state, build_state_dict(position, dx, dy, 0, 0, "evade", target1_type, target1_distance, target1_angle,
                                                               danger_type, danger_distance, danger_angle)


def scan_for_targets(values, main_target, secondary_target):
    """
    Scans the play area for the targets using their last known coordinates.
    It uses a two pass scan to find the targets. First, it checks around the last known position to find the
    target again, making sure to always follow the target as long as nothing gets in the way. The second scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param main_target: The main target type to search for
    :param secondary_target: The secondary target type to scan for
    :return: The information on the main target in four variables and the information about the secondary target
    in four variables.
    """
    target1_type = "\x00\x00"
    target1_distance = (0, 0)
    target1_angle = 0
    target1_info = 0
    target2_type = "\x00\x00"
    target2_distance = (0, 0)
    target2_angle = 0
    target2_info = 0

    # Check if we have a targeted player for scanning
    if values[1] != "\x00\x00" and values[2] != "\x00\x00" and values[3] != "\x00\x00":
        target1_type = values[1]
        target1_distance = (ord(values[2][:1]) - arena_dimensions[0], ord(values[2][1:]) - arena_dimensions[1])
        target1_angle = ord(values[3][:1])

    # Check if we have a targeted weapon
    if values[4] != "\x00\x00" and values[5] != "\x00\x00" and values[6] != "\x00\x00":
        target2_type = values[4]
        target2_distance = (ord(values[5][:1]) - arena_dimensions[0], ord(values[5][1:]) - arena_dimensions[1])
        target2_angle = ord(values[6][:1])

    if target1_type == types[main_target]:
        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in range(
                max(int(target1_angle) - small_scan_range, 0),
                min(int(target1_angle) + small_scan_range, 359),
                1,
        ):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if entity_type == main_target:
                found = True
                target1_type = types[entity_type]
                target1_distance = distance_compo
                target1_angle = angle
                target1_info = info
            if entity_type == secondary_target and (empty_tupple(target2_distance)
                                                    or compare_distance(distance_compo, target2_distance)):
                # If we found a secondary target, still save it
                target2_type = types[entity_type]
                target2_distance = distance_compo
                target2_angle = angle
                target2_info = info

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target1_type = "\x00\x00"
            target1_distance = (0, 0)
            target1_angle = 0

    if target2_type == types[secondary_target]:
        # Scan in the vicinity of the secondary_target last known position
        found = False
        for angle in range(
                max(int(target2_angle) - small_scan_range, 0),
                min(int(target2_angle) + small_scan_range, 359),
                1,
        ):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if entity_type == secondary_target and (empty_tupple(target2_distance)
                                                    or compare_distance(distance_compo, target2_distance)):
                found = True
                target2_type = types[entity_type]
                target2_distance = distance_compo
                target2_angle = angle
                target2_info = info

        # If we still couldn't find the secondary target, we lost it, reset that target
        if not found:
            target2_type = "\x00\x00"
            target2_distance = (0, 0)
            target2_angle = 0

    # If we should still scan around us
    if not target1_type == types[main_target] or not target2_type == types[secondary_target]:
        # Do a 90 degrees scan in a random quadrant
        random_angle = random.randint(0, 3) * 90
        for angle in range(random_angle, min(random_angle + 90, 359), 1):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            # Scan for both our target without any priority.
            if entity_type == main_target:
                target1_type = types[entity_type]
                target1_distance = distance_compo
                target1_angle = angle
                target1_info = info
            if entity_type == secondary_target and (empty_tupple(target2_distance)
                                                    or compare_distance(distance_compo, target2_distance)):
                target2_type = types[entity_type]
                target2_distance = distance_compo
                target2_angle = angle
                target2_info = info

    return target1_type, target1_distance, target1_angle, target1_info,\
        target2_type, target2_distance, target2_angle, target2_info


def scan_for_danger(position, velocity):
    """
    Scan towards the position the agent is moving to for any obstacles or dangers
    :param position: Current position of the agent for wall detection
    :param velocity: Current velocity of the agent for object detection
    :return: Whether or not there is danger ahead
    """
    if position[0] - acceptable_distance < 0:
        return True, types["wall"], (
            0,
            position[1],
        ), 0
    if position[0] + acceptable_distance > arena_dimensions[0]:
        return True, types["wall"], (
            arena_dimensions[0],
            position[1],
        ), 0
    if position[1] - acceptable_distance < 0:
        return True, types["wall"], (
            position[0],
            0,
        ), 0
    if position[1] + acceptable_distance > arena_dimensions[1]:
        return True, types["wall"], (
            position[0],
            arena_dimensions[1],
        ), 0

    agent_angle = math.degrees(math.atan2(velocity[1], velocity[0]))

    for angle in range(max(int(agent_angle) - small_scan_range, 0), min(int(agent_angle) + small_scan_range, 359), 1):
        (entity_type, distance, info) = get_the_radar_data(angle)

        if (entity_type == "player" or entity_type == "column" or entity_type == "hazard")\
                and distance < acceptable_distance:
            return True, types[entity_type], vector_to_components(distance, angle), angle

        if entity_type == "weapon" and distance < acceptable_distance and info:
            return True, types[entity_type], vector_to_components(distance, angle), angle

    return False, "\x00\x00", (0, 0), 0


def build_state_dict(position, dx, dy, rot_cc, rot_cw, current_state, target1_type, target1_distance, target1_angle,
                     target2_type, target2_distance, target2_angle):
    """
    Create the dictionnary to send back to the game using the base info
    :param position: The current position of the agent for line drawing purposes
    :param dx: The desired horizontal velocity
    :param dy: The desired vertical velocity
    :param rot_cc: The desired counter clock wise rotation
    :param rot_cw: The desired clock wise rotation
    :param current_state: The current state of the agent
    :param target1_type: The type of the main target
    :param target1_distance: The distance of the main target to the agent
    :param target1_angle: The angle of the main target from the agent.
    :param target2_type: The type of the secondary target
    :param target2_distance: The distance of the secondary target to the agent
    :param target2_angle: The angle of the secondary target from the agent.
    :return: A disctionare ready to be sent to the game
    """
    return {
        'ACLT_X': dx,
        'ACLT_Y': dy,
        'ROT_CC': rot_cc,
        'ROT_CW': rot_cw,
        'SAVE_A': states[current_state],
        'SAVE_B': target1_type,
        'SAVE_C': chr(
            int(arena_dimensions[0] + target1_distance[0])
        ) + chr(int(arena_dimensions[1] + target1_distance[1])),
        'SAVE_D': chr(int(target1_angle)) + "0",
        'SAVE_E': target2_type,
        'SAVE_F': chr(
            int(arena_dimensions[0] + target2_distance[0])
        ) + chr(int(arena_dimensions[1] + target2_distance[1])),
        'SAVE_X': chr(int(target2_angle)) + "0",
        # Write debug lines to the found player and weapon
        'DEBUGS': [
            (
                int(position[0]),
                int(position[1]),
                int(target1_distance[0] + position[0]),
                int(target1_distance[1] + position[1]),
            ),
            (
                int(position[0]),
                int(position[1]),
                int(target2_distance[0] + position[0]),
                int(target2_distance[1] + position[1])
            ),
        ]
    }

def vector_to_components(magnitude, angle):
    """
    Returns the component representation of a vector
    :param magnitude: The magnitude of the vector
    :param angle: The angle of the vector
    :return: The component representation in a tupple
    """
    return(
        magnitude * math.cos(math.radians(angle)),
        magnitude * math.sin(math.radians(angle)),
    )


def compare_distance(distance1, distance2):
    """
    Returns if the distance 1 is smaller than distance 2
    :param distance1: The first distance to compare
    :param distance2: The second distance to compare
    :return: Whether or not the first distance is closer
    """
    return (distance1[0] ** 2 + distance1[1] ** 2) <= (distance2[0] ** 2 + distance2[1] ** 2)


def empty_tupple(tupple):
    """
    Check if the tupple is empty by checking if both it's component are == 0
    :param tupple: The tupple to check
    :return: Whether or not that tupple is empty
    """
    return tupple[0] == 0 and tupple[1] == 0
