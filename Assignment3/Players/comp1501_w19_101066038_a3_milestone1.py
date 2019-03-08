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
# In the wander state, the agent will scan for a target nd stop moving to better position itself. If the agent detects a
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

arena_dimensions = (750,  750)

acceptable_distance = 60

disengage_distance = 150

fire_distance = 200

small_scan_range = 15
danger_scan_range = 30

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
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_closest_target(values, 4, 5, 6, "weapon")

    # If a weapon is in view and we don't have a weapon, change state to go grab it
    if target2_type == types["weapon"] and not get_if_have_weapon():
        next_state = "w_get_weapon"

    # Check if we have a weapon
    if get_if_have_weapon():
        # move to the aggressive state
        next_state = "a_wander"

    # Check if the player is dangerous
    if target2_type == types["player"] and target1_info[1]:
        # move to the cautious state
        next_state = "c_wander"

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
    """
    The get_weapon state of the WANDER main state, identified by the chars 0G. This state makes the agent moves
    towards the nearest weapon while still keeping an eye on the player.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_get_weapon("w_", "player")


def w_evade():
    """
    The evade state of the WANDER main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("w_", "player")


def c_wander():
    """
    The wander state of the CAUTIOUS main state, identified by the chars 0W. This state makes the agent move
    perpendicular to the last know position of the player while looking for the nearest column. It will save the
    position of the player as target 1 and the column as target 2. If no player is found, it will look for a weapon
    and move towards it.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "c_wander"

    # Scan for a player and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_closest_target(values, 4, 5, 6, "column")

    # Check if we have a weapon
    if get_if_have_weapon():
        # move to the aggressive state
        next_state = "a_wander"

    # If a column is in view and the player is still dangerous, go hide
    if target1_type == types["player"] and target2_type == types["column"] and target1_info[1]:
        next_state = "c_hide"
    # If the player is not dangerous anymore
    elif target1_type == types["player"] and not target1_info[1]:
        next_state = "w_wander"
    # If we couldn't find a player, look for a weapon
    elif target1_type != types["player"]:
        (target1_type, target1_distance, target1_angle, target1_info) =\
            scan_for_closest_target(values, 1, 2, 3, "weapon")
        if target1_type != types["weapon"]:
            next_state = "c_get_weapon"

    # Move perpendicular to the player if any
    dx = cos(radians(target1_angle))
    dy = sin(radians(target1_angle))
    if dx > dy:
        dy = 0
    else:
        dx = 0

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
        next_state = "c_evade"
        target2_type = danger_type
        target2_distance = danger_distance
        target2_angle = danger_angle

    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle)


def c_hide():
    """
    The hide state of the CAUTIOUS main state, identified by the chars 0H. THis state makes the agent try to put a
    column between it and the detected player. It will also slightly move towards that column if within a reasonable
    distance. If it cannot detect any player, it will move towards the peek state to find them.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "c_hide"

    # Scan for a player and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    if values[4] != types["column"]:
        (target2_type, target2_distance, target2_angle, target2_info)\
            = scan_for_closest_target(values, 4, 5, 6, "column")
    else:
        (target2_type, target2_distance, target2_angle, target2_info) = scan_for_target(values, 4, 5, 6, "column")

    # If we couldn't find a player
    if target1_type != types["player"]:
        # Peek before wandering
        next_state = "c_peek"

    # If we couldn't find a column
    if target2_type != types["column"]:
        # Why are we even here? Resume wandering
        next_state = "c_wander"

    # If the player if not dangerous anymore
    if target1_type == types["player"] and not target1_info[1]:
        next_state = "w_wander"

    # Find a point behind the column
    player_to_col_vector = (
        target2_distance[0] - target1_distance[0],
        target2_distance[1] - target1_distance[1],
    )
    vector_length = sqrt(player_to_col_vector[0] ** 2 + player_to_col_vector[1] ** 2)
    direction = (player_to_col_vector[0] / vector_length, player_to_col_vector[1] / vector_length)
    vector_behind_col = (
        target2_distance[0] + direction[0] * acceptable_distance,
        target2_distance[1] + direction[1] * acceptable_distance
    )

    steps_number = max(abs(vector_behind_col[0]), abs(vector_behind_col[1]))

    # Move towards that point
    dx = float(vector_behind_col[0]) / steps_number
    dy = float(vector_behind_col[1]) / steps_number

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
        next_state = "c_evade"
        target1_type = danger_type
        target1_distance = danger_distance
        target1_angle = danger_angle

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "hide", target1_type, target1_distance,
                                  target1_angle, target2_type, target2_distance, target2_angle)
    state_dict["DEBUGS"].append((
        int(position[0]),
        int(position[1]),
        int(position[0] + vector_behind_col[0]),
        int(position[1] + vector_behind_col[1]),
    ))

    return next_state, state_dict


def c_peek():
    """
    The peek state of the CAUTIOUS main state, identified by the chars 0P. This state makes the agent move away from
    the column they are standing near until they can find a player or are too far away from the column. If they move
    too far away, the agent will move to the wander state. If they found a player, they will resume th hide state.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "c_peek"

    # Scan for a player and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_target(values, 4, 5, 6, "column")

    # If we could find a player and they're dangerous
    if target1_type == types["player"] and target1_info[1]:
        # Return hiding
        next_state = "c_hide"
    # If the player if not dangerous anymore
    elif target1_type == types["player"] and not target1_info[1]:
        next_state = "w_wander"

    # If we couldn't find a column or if we're too far from the column
    if target2_type != types["column"]\
            or (target2_type == types["column"] and
                target2_distance[0] ** 2 + target2_distance[1] ** 2 >= disengage_distance ** 2):
        next_state = "c_wander"

    # Move away from the column
    dx = -cos(radians(target2_angle))
    dy = -sin(radians(target2_angle))

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
        next_state = "c_evade"
        target1_type = danger_type
        target1_distance = danger_distance
        target1_angle = danger_angle

    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "peek", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle)


def c_get_weapon():
    """
    The get_weapon state of the WANDER main state, identified by the chars 0G. This state makes the agent moves
    towards the nearest weapon while still keeping an eye on the player.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_get_weapon("c_", "player")


def c_evade():
    """
    The evade state of the CAUTIOUS main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("c_", "column")


def a_wander():
    """
    The wander state of the AGGRESSIVE main state, identified by the chars 0W. This state makes the agent stop moving
    and look for an enemy to show up.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "a_wander"

    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_closest_target(values, 4, 5, 6, "weapon")

    # If we don't have a weapon
    if get_if_have_weapon():
        # What are we doing here? Move to the best main state for this case
        if target1_type == types["player"] and target1_info[1]:
            next_state = "c_wander"
        else:
            next_state = "a_wander"

    # If we found a player, move to the the go behind state
    if target1_type == types["player"]:
        next_state = "a_go_behind"

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

    return next_state, build_state_dict(position, 0, 0, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle)


def a_go_behind():
    """
    The go_behind state of the AGGRESSIVE main state, identified by the chars 0B. This state makes the agent move to
    position itself out of reach of the firing line of the player while trying to get behind them. Once it has reach
    firing distance, ot will fire its weapon towards the enemy and commit to it.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "a_go_behind"

    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_target(values, 1, 2, 3, "weapon")

    # If we don't have a weapon
    if get_if_have_weapon():
        # What are we doing here? Move to the best main state for this case
        if target1_type == types["player"] and target1_info[1]:
            next_state = "c_wander"
        else:
            next_state = "a_wander"

    # If we couldn't find a player, return to wander
    if target1_type != types["player"]:
        next_state = "a_wander"

    # If we found a player, turn to face it and move towards its back
    rot_cc = 0
    rot_cw = 0
    dx = 0
    dy = 0
    debug_line = ()
    if target1_type == types["player"]:
        # If within firing distance, also commit to firing
        if (target1_distance[0] ** 2 + target2_distance[1] ** 2) <= fire_distance ** 2:
            next_state = "a_fire"

        # Get current angle and compare it with the desired angle
        throw = get_throwing_angle()
        delta = ((target1_angle - throw) + 360) % 360

        if delta > 180:
            rot_cc = 0
            rot_cw = 1
        else:
            rot_cc = 1
            rot_cw = 0

        # Get the player angle and do some vector math
        player_angle = target1_info[2]
        behind_vector = vector_to_components(acceptable_distance, player_angle)

        # Find a point behind the player_angle
        player_to_behind_vector = (
            behind_vector[0] - target1_distance[0],
            behind_vector[1] - target1_distance[1],
        )
        vector_length = sqrt(player_to_behind_vector[0] ** 2 + player_to_behind_vector[1] ** 2)
        direction = (player_to_behind_vector[0] / vector_length, player_to_behind_vector[1] / vector_length)
        vector_behind = (
            behind_vector[0] + direction[0] * acceptable_distance,
            behind_vector[1] + direction[1] * acceptable_distance
        )

        steps_number = max(abs(vector_behind[0]), abs(vector_behind[1]))

        # Move towards that point
        dx = float(vector_behind[0]) / steps_number
        dy = float(vector_behind[1]) / steps_number

        debug_line = (
            int(position[0]),
            int(position[1]),
            int(position[0] + vector_behind[0]),
            int(position[1] + vector_behind[1]),
        )

    # Make sure we evade anything we're moving towards
    (danger, danger_type, danger_distance, danger_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "w_evade"
        target2_type = danger_type
        target2_distance = danger_distance
        target2_angle = danger_angle

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "hide", target1_type, target1_distance,
                                  target1_angle, target2_type, target2_distance, target2_angle)
    state_dict["DEBUGS"].append(debug_line)

    return next_state, state_dict


def a_fire():
    """
    The fire state of the AGGRESSIVE main state, identified by the chars 0F. This state makes the agent move to
    position itself out of reach of the firing line of the player and align itself to the enemy player.
    Once aligned and within range, it will fire its weapon and revert to the best state for the situation
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "a_fire"

    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, "player")
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_target(values, 1, 2, 3, "weapon")

    # If we don't have a weapon
    if get_if_have_weapon():
        # What are we doing here? Move to the best main state for this case
        if target1_type == types["player"] and target1_info[1]:
            next_state = "c_wander"
        else:
            next_state = "a_wander"

    # If we couldn't find a player, return to wander
    if target1_type != types["player"]:
        next_state = "a_wander"

    # If we found a player, turn to face it and move towards its back
    rot_cc = 0
    rot_cw = 0
    dx = 0
    dy = 0
    fire = False
    debug_line = (0, 0)
    if target1_type == types["player"]:
        # If not within firing distance, return to moving towards it
        if (target1_distance[0] ** 2 + target2_distance[1] ** 2) > fire_distance ** 2:
            next_state = "a_go_behind"

        # Get current angle and compare it with the desired angle
        throw = get_throwing_angle()
        delta = ((target1_angle - throw) + 360) % 360

        if delta > 180:
            rot_cc = 0
            rot_cw = 1
        else:
            rot_cc = 1
            rot_cw = 0

        # Get the player angle and do some vector math
        player_angle = target1_info[2]
        behind_vector = vector_to_components(acceptable_distance, player_angle)

        # Find a point behind the player_angle
        player_to_behind_vector = (
            behind_vector[0] - target1_distance[0],
            behind_vector[1] - target1_distance[1],
        )
        vector_length = sqrt(player_to_behind_vector[0] ** 2 + player_to_behind_vector[1] ** 2)
        direction = (player_to_behind_vector[0] / vector_length, player_to_behind_vector[1] / vector_length)
        vector_behind = (
            behind_vector[0] + direction[0] * acceptable_distance,
            behind_vector[1] + direction[1] * acceptable_distance
        )

        steps_number = max(abs(vector_behind[0]), abs(vector_behind[1]))

        # Move towards that point
        dx = float(vector_behind[0]) / steps_number
        dy = float(vector_behind[1]) / steps_number

        debug_line = (
            int(position[0]),
            int(position[1]),
            int(position[0] + vector_behind[0]),
            int(position[1] + vector_behind[1]),
        )

        # If we can directly see the player in our current angle
        (target_type, _, target_info) = get_the_radar_data(throw)
        if target_type == types["player"]:
            # Fire!
            fire = True
            if target1_info[1]:
                # Become cautious if the player is armed
                next_state = "c_wander"
            else:
                # Otherwise, wander
                next_state = "w_wander"

    # Make sure we evade anything we're moving towards
    (danger, danger_type, danger_distance, danger_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "w_evade"
        target2_type = danger_type
        target2_distance = danger_distance
        target2_angle = danger_angle

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "hide", target1_type, target1_distance,
                                  target1_angle, target2_type, target2_distance, target2_angle)
    state_dict["DEBUGS"].append(debug_line)

    # If firing, relase the weapon
    if fire:
        state_dict["WEAPON"] = False

    return next_state, state_dict


def a_evade():
    """
    The evade state of the AGRESSIVE main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("a_", "player")


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
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, main_target)
    (weapon_type, weapon_distance, weapon_angle, weapon_info) = scan_for_target(values, 4, 5, 6, "weapon")

    # Check if we have a weapon
    if get_if_have_weapon():
        # move to the aggressive state
        return "a_wander", build_state_dict(position, 0, 0, 0, 0, "get_weapon", target1_type, target1_distance,
                                            target1_angle, weapon_type, weapon_distance, weapon_angle)

    # Check if we found a player and it was dangerous
    if target1_type == types["player"] and target1_info[1]:
        # move to the cautious state
        next_state = "c_wander"

    # If the weapon is dangerous or could not be found
    if weapon_type != types["weapon"] or weapon_info:
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

        (weapon_type, weapon_distance, weapon_angle, weapon_info) = scan_for_target(new_values, 4, 5, 6, "weapon")

    # If the weapon could still not be found or is still dangerous
    if weapon_type != types["weapon"] or weapon_info:
        # Return to the previous state
        return main_state + "wander", build_state_dict(position, 0, 0, 0, 0, "get_weapon", target1_type,
                                                       target1_distance, target1_angle, weapon_type, weapon_distance,
                                                       weapon_angle)

    # Else, move towards it
    dx = cos(radians(weapon_angle))
    dy = sin(radians(weapon_angle))

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
        next_state = main_state + "evade"
        weapon_type = danger_type
        weapon_distance = danger_distance
        weapon_angle = danger_angle

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "get_weapon", target1_type, target1_distance,
                                  target1_angle, weapon_type, weapon_distance, weapon_angle)
    state_dict["WEAPON"] = True

    return next_state, state_dict


def shared_evade(main_state, primary_target):
    """
    This shared evade code allows the multiple evade states to hare their base code. Evade makes the agent flee
    the nearest hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = main_state + "evade"

    # Scan for the two given targets
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_target(values, 1, 2, 3, primary_target)

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

        dx = cos(radians(target_angle))
        dy = sin(radians(target_angle))

    # Make sure we evade anything we're moving towards
    (danger, danger_type, danger_distance, danger_angle) = scan_for_danger(position, get_velocity_tuple())
    if not danger:
        next_state = main_state + reverse_states[values[0]]

    return next_state, build_state_dict(position, dx, dy, 0, 0, reverse_states[values[0]], target1_type,
                                        target1_distance, target1_angle, danger_type, danger_distance, danger_angle)


def scan_for_target(values, type_index, distance_index, angle_index, searched_type):
    """
    Scans the play area for the target using its last known coordinates.
    It uses a two pass scan to find the target. First, it checks around the last known position to find the
    target again, making sure to always follow the target as long as nothing gets in the way. The second scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param type_index: The index of the target's type in the values array
    :param distance_index: The index of the target's distance in the values array
    :param angle_index: The index of the target's angle in the values array
    :param searched_type: The main target type to search for
    :return: The information on the main target in four variables
    """
    target_type = "\x00\x00"
    target_distance = (0, 0)
    target_angle = 0
    target_info = 0

    # Check if we have a targeted main target for scanning
    if values[type_index] != "\x00\x00" and values[distance_index] != "\x00\x00" and values[angle_index] != "\x00\x00":
        target_type = values[type_index]
        target_distance = (
            ord(values[distance_index][:1]) - arena_dimensions[0],
            ord(values[distance_index][1:]) - arena_dimensions[1],
        )
        target_angle = ord(values[angle_index][:1])

    if target_type == types[searched_type]:
        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in angle_range(target_angle, small_scan_range):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if entity_type == searched_type:
                found = True
                target_type = types[entity_type]
                target_distance = distance_compo
                target_angle = angle
                target_info = info

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target_type = "\x00\x00"
            target_distance = (0, 0)
            target_angle = 0

    # If we should still scan around us
    if not target_type == types[searched_type]:
        # Do a 90 degrees scan in a random quadrant
        random_angle = randint(0, 3) * 90
        for angle in angle_range(random_angle, 90):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            # Scan for both our target without any priority.
            if entity_type == searched_type:
                target_type = types[entity_type]
                target_distance = distance_compo
                target_angle = angle
                target_info = info

    return target_type, target_distance, target_angle, target_info


def scan_for_closest_target(values, type_index, distance_index, angle_index, searched_type):
    """
    Scans the play area for the target using its last known coordinates and making sure the found target is the closest
    to the player. It uses a three pass scan to find the target. First, it checks around the last known position to find
    the target again, making sure to always follow the target as long as nothing gets in the way. The second scan looks
    in a 90 degrees area around the target last known position in case it went faster. The third scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param type_index: The index of the target's type in the values array
    :param distance_index: The index of the target's distance in the values array
    :param angle_index: The index of the target's angle in the values array
    :param searched_type: The main target type to search for
    :return: The information on the main target in four variables
    """
    target_type = "\x00\x00"
    target_distance = (0, 0)
    target_angle = 0
    target_info = 0

    # Check if we have a targeted main target for scanning
    if values[type_index] != "\x00\x00" and values[distance_index] != "\x00\x00" and values[angle_index] != "\x00\x00":
        target_type = values[type_index]
        target_distance = (
            ord(values[distance_index][:1]) - arena_dimensions[0],
            ord(values[distance_index][1:]) - arena_dimensions[1],
        )
        target_angle = ord(values[angle_index][:1])

    if target_type == types[searched_type]:
        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in angle_range(target_angle, small_scan_range):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if entity_type == searched_type and\
                    (empty_tupple(target_distance) or compare_distance(distance_compo, target_distance)):
                found = True
                target_type = types[entity_type]
                target_distance = distance_compo
                target_angle = angle
                target_info = info

        # If we could find the target, try a 90 degrees scan
        if not found:
            for angle in angle_range(target_angle, 90):
                (entity_type, distance, info) = get_the_radar_data(angle)
                distance_compo = vector_to_components(distance, angle)

                if entity_type == searched_type and \
                        (empty_tupple(target_distance) or compare_distance(distance_compo, target_distance)):
                    found = True
                    target_type = types[entity_type]
                    target_distance = distance_compo
                    target_angle = angle
                    target_info = info

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target_type = "\x00\x00"
            target_distance = (0, 0)
            target_angle = 0

    # If we should still scan around us
    if not target_type == types[searched_type]:
        # Do a 90 degrees scan in a random quadrant
        random_angle = randint(0, 3) * 90
        for angle in angle_range(random_angle, 90):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            # Scan for both our target without any priority.
            if entity_type == searched_type and\
                    (empty_tupple(target_distance) or compare_distance(distance_compo, target_distance)):
                target_type = types[entity_type]
                target_distance = distance_compo
                target_angle = angle
                target_info = info

    return target_type, target_distance, target_angle, target_info


def scan_for_danger(position, velocity):
    """
    Scan towards the position the agent is moving to for any obstacles or dangers
    :param position: Current position of the agent for wall detection
    :param velocity: Current velocity of the agent for object detection
    :return: Whether or not there is danger ahead
    """
    if position[0] - acceptable_distance < 0:
        return True, types["wall"], (
            -position[0],
            0,
        ), 180
    if position[0] + acceptable_distance > arena_dimensions[0]:
        return True, types["wall"], (
            arena_dimensions[0] - position[0],
            0,
        ), 90
    if position[1] - acceptable_distance < 0:
        return True, types["wall"], (
            0,
            -position[1],
        ), 270
    if position[1] + acceptable_distance > arena_dimensions[1]:
        return True, types["wall"], (
            0,
            arena_dimensions[1] - position[1],
        ), 0

    agent_angle = int(degrees(atan2(velocity[1], velocity[0])))

    for angle in angle_range(agent_angle, danger_scan_range):
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
    :return: A dictionary ready to be sent to the game
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


def angle_range(angle, wanted_range):
    """
    Creates an array to iterate over from the given angle and the range of degrees. The function with find a range of
    the size of the wanted range with the angle in the middle.
    :param angle: The given angle to place in the middle of the range
    :param wanted_range: The size of the angle range to look for, max 359 degrees.
    :return: An array containing all the angles in the range for a for loop.
    """
    got_range = []
    for i in range(angle - wanted_range // 2, angle + wanted_range // 2, 1):
        got_range.append(i if angle > 0 else 359 - i)

    return got_range


def vector_to_components(magnitude, angle):
    """
    Returns the component representation of a vector
    :param magnitude: The magnitude of the vector
    :param angle: The angle of the vector
    :return: The component representation in a tupple
    """
    return(
        magnitude * cos(radians(angle)),
        magnitude * sin(radians(angle)),
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
