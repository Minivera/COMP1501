# -> AGRECO
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
# SAVE_B: Target 1 type and angle as two unicode characters.
# SAVE_C: Target 1 distance as a two unicode characters (x, y). Convert the char to an int. Offset of 750.
# SAVE_D: Target 2 type and angle as two unicode characters.
# SAVE_E: Target 2 distance as a two unicode characters (x, y). Convert the char to an int. Offset of 750.
# SAVE_F: Target 3 type and angle as two unicode characters.
# SAVE_X: Target 3 distance as a two unicode characters (x, y). Convert the char to an int. Offset of 750.
# SAVE_Y: Reserved

arena_dimensions = (750,  750)

acceptable_distance = 60

disengage_distance = 150

fire_distance = 200

caution_threshold = 50

small_scan_range = 30
danger_scan_range = 30

types = {
    "column": "C",
    "player": "P",
    "weapon": "W",
    "hazard": "H",
    "wall": "M",
}

reverse_types = {
    "C": "column",
    "P": "player",
    "W": "weapon",
    "H": "hazard",
    "M": "wall",
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

    debug_circle = []
    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_weapon(values, debug_circle)

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
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "w_evade"

    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                        target3_distance, target3_angle, debug_circle)


def w_get_weapon():
    """
    The get_weapon state of the WANDER main state, identified by the chars 0G. This state makes the agent moves
    towards the nearest weapon while still keeping an eye on the player.
    :return: The next state and a dictionary of information to send back to the game.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "w_get_weapon"

    debug_circle = []
    # Scan for a weapon and optionally the other target
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (weapon_type, weapon_distance, weapon_angle, weapon_info) = scan_for_weapon(values, debug_circle)

    # Check if we have a weapon
    if get_if_have_weapon():
        # move to the aggressive state
        next_state = "a_wander"

    # Check if we found a player and it was dangerous
    if target1_type == types["player"] and target1_info[1]:
        # move to the cautious state
        next_state = "c_wander"

    # If the weapon is dangerous or could not be found
    if weapon_type != types["weapon"] or weapon_info:
        # return to previous state
        next_state = "w_" + reverse_states[values[0]]

    # Make sure we evade anything we're moving towards
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "w_evade"

    # If the weapon could still not be found or is still dangerous
    if weapon_type != types["weapon"] or weapon_info:
        # Return to the previous state
        return "w_wander", build_state_dict(position, 0, 0, 0, 0, "get_weapon", target1_type,
                                            target1_distance, target1_angle, weapon_type, weapon_distance,
                                            weapon_angle, target3_type, target3_distance, target3_angle,
                                            debug_circle)

    # Else, move towards it
    steps_number = max(abs(weapon_distance[0]), abs(weapon_distance[1]))

    dx = float(weapon_distance[0]) / steps_number
    dy = float(weapon_distance[1]) / steps_number

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

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "get_weapon", target1_type, target1_distance,
                                  target1_angle, weapon_type, weapon_distance, weapon_angle, target3_type,
                                  target3_distance, target3_angle, debug_circle)
    state_dict["WEAPON"] = True

    return next_state, state_dict


def w_evade():
    """
    The evade state of the WANDER main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("w_")


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

    debug_circle = []
    # Scan for a player, a weapon and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_column(values, debug_circle)

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

    target1_angle += 90
    if target1_angle > 359:
        target1_angle = 0 + (target1_angle - 359)
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
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "c_evade"

    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                        target3_distance, target3_angle, debug_circle)


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

    debug_circle = []
    # Scan for a player, a weapon and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, _) = scan_for_column(values, debug_circle)

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

    # Make sure we stay far from the column if too close
    if (target2_distance[0] ** 2 + target2_distance[1] ** 2) <= acceptable_distance ** 2:
        dx -= cos(radians(target2_angle))
        dy -= sin(radians(target2_angle))

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
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "c_evade"

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "hide", target1_type, target1_distance,
                                  target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                  target3_distance, target3_angle, debug_circle)
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

    debug_circle = []
    # Scan for a player, a weapon and a column
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, _) = scan_for_column(values, debug_circle)

    # If we could find a player and they're dangerous
    if target1_type == types["player"] and target1_info[1]:
        # Return hiding
        next_state = "c_hide"
    # If the player if not dangerous anymore
    elif target1_type == types["player"] and not target1_info[1]:
        next_state = "w_wander"

    # If we couldn't find a column or if we're too far from the column
    if target2_type != types["column"]:
        # Return to wandering
        next_state = "c_wander"

    # If we found a column and we're strifing too far from it, return to hide
    if target2_type == types["column"] and \
            target2_distance[0] ** 2 + target2_distance[1] ** 2 >= disengage_distance ** 2:
        next_state = "c_hide"

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
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "c_evade"

    return next_state, build_state_dict(position, dx, dy, rot_cc, rot_cw, "peek", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                        target3_distance, target3_angle, debug_circle)


def c_evade():
    """
    The evade state of the CAUTIOUS main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("c_")


def a_wander():
    """
    The wander state of the AGGRESSIVE main state, identified by the chars 0W. This state makes the agent stop moving
    and look for an enemy to show up.
    :return: Returns the next state and a dictionary with instructions
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = "a_wander"

    debug_circle = []
    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_weapon(values, debug_circle)

    # If we don't have a weapon
    if not get_if_have_weapon():
        # What are we doing here? Move to the best main state for this case
        if target1_type == types["player"] and target1_info[1]:
            next_state = "c_wander"
        else:
            next_state = "w_wander"

    # If we found a player and they're not dangerous, move to the the go behind state
    if target1_type == types["player"] and not target1_info[1]:
        next_state = "a_go_behind"
    # Otherwise if they're dangerous and we're low on health, be more cautious
    elif target1_type == types["player"] and get_current_status() <= caution_threshold and target1_info[1]:
        next_state = "c_wander"

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
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "a_evade"

    return next_state, build_state_dict(position, 0, 0, rot_cc, rot_cw, "wander", target1_type, target1_distance,
                                        target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                        target3_distance, target3_angle, debug_circle)


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

    debug_circle = []
    # Scan for a player and optionally a weapon
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, target2_info) = scan_for_weapon(values, debug_circle)

    # If we don't have a weapon
    if not get_if_have_weapon():
        # What are we doing here? Move to the best main state for this case
        if target1_type == types["player"] and target1_info[1]:
            next_state = "c_wander"
        else:
            next_state = "w_wander"

    # If we couldn't find a player, return to wander
    if target1_type != types["player"]:
        next_state = "a_wander"

    # If we could find a player, they're dangerous and we're low on health, be more cautious
    if target1_type == types["player"] and get_current_status() <= caution_threshold and target1_info[1]:
        next_state = "c_wander"

    # If we found a player, turn to face it and move towards its back
    rot_cc = 0
    rot_cw = 0
    dx = 0
    dy = 0
    debug_line = ()
    fire = False
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

        # Get the player angle and do some vector math
        player_angle = target1_info[2]
        behind_vector = vector_to_components(acceptable_distance, invert_angle(player_angle))

        # Find a point behind the player_angle
        player_to_behind_vector = (
            behind_vector[0] + target1_distance[0],
            behind_vector[1] + target1_distance[1],
        )

        steps_number = max(abs(player_to_behind_vector[0]), abs(player_to_behind_vector[1]))

        # Move towards that point
        dx = float(player_to_behind_vector[0]) / steps_number
        dy = float(player_to_behind_vector[1]) / steps_number

        debug_line = (
            int(position[0]),
            int(position[1]),
            int(position[0] + player_to_behind_vector[0]),
            int(position[1] + player_to_behind_vector[1]),
        )

        # If we can directly see the player in our current angle and within fire distance
        if (delta < 1 or delta > 359) and abs(target1_distance[0] ** 2 + target1_distance[1] ** 2) < fire_distance ** 2:
            # Fire!
            fire = True
            if target1_info[1]:
                # Become cautious if the player is armed
                next_state = "c_wander"
            else:
                # Otherwise, wander
                next_state = "w_wander"

    # Make sure we evade anything we're moving towards
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if danger:
        next_state = "a_evade"

    state_dict = build_state_dict(position, dx, dy, rot_cc, rot_cw, "go_behind", target1_type, target1_distance,
                                  target1_angle, target2_type, target2_distance, target2_angle, target3_type,
                                  target3_distance, target3_angle, debug_circle)
    state_dict["DEBUGS"].append(debug_line)

    # If firing, release the weapon
    if fire:
        state_dict["WEAPON"] = False

    return next_state, state_dict


def a_evade():
    """
    The evade state of the AGRESSIVE main state, identified by the chars 0E. This state makes the agent flee the nearest
    hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    return shared_evade("a_")


def shared_evade(main_state):
    """
    This shared evade code allows the multiple evade states to hare their base code. Evade makes the agent flee
    the nearest hazard or bounce away from the nearest wall.
    :return: The next state and a dictionary of information to send back to the game.
    """
    position = get_position_tuple()
    values = get_my_stored_data()
    next_state = main_state + "evade"

    debug_circle = []
    # Scan for the two given targets
    (target1_type, target1_distance, target1_angle, target1_info) = scan_for_player(values, debug_circle)
    (target2_type, target2_distance, target2_angle, _) = scan_for_weapon(values, debug_circle)

    target3_type = "\x00"
    target3_angle = 0

    # Check if we have a targeted hazard
    if values[5] != "\x00\x00" and values[6] != "\x00\x00":
        target3_type = values[5][:1]
        target3_angle = ord(values[5][1:])

    dx = 0
    dy = 0
    # Accelerate away from danger if any is saved
    if target3_type != "\x00":
        target_angle = invert_angle(target3_angle)

        dx = cos(radians(target_angle))
        dy = sin(radians(target_angle))

    # Make sure we evade anything we're moving towards
    (danger, target3_type, target3_distance, target3_angle) = scan_for_danger(position, get_velocity_tuple())
    if not danger:
        next_state = main_state + reverse_states[values[0]]

    return next_state, build_state_dict(position, dx, dy, 0, 0, reverse_states[values[0]], target1_type,
                                        target1_distance, target1_angle, target2_type, target2_distance, target2_angle,
                                        target3_type, target3_distance, target3_angle, debug_circle)


def scan_for_player(values, debug_circles):
    """
    Scans the play area for the target using its last known coordinates.
    It uses a two pass scan to find the target. First, it checks around the last known position to find the
    target again, making sure to always follow the target as long as nothing gets in the way. The second scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param debug_circles: An array to add any circle info for debugging. Will add a tuple with the target distance
    and the scan circle.
    :return: The information on the main target in four variables
    """
    target_type = "\x00"
    target_distance = (0, 0)
    target_angle = 0
    target_info = 0

    # Check if we have a targeted main target for scanning
    if values[1] != "\x00\x00" and values[2] != "\x00\x00":
        target_type = values[1][:1]
        target_angle = ord(values[1][1:])
        target_distance = (
            ord(values[2][:1]) - arena_dimensions[0],
            ord(values[2][1:]) - arena_dimensions[1],
        )

    if target_type == types["player"]:
        debug_circles.append((target_distance, small_scan_range))

        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in angle_range(target_angle, small_scan_range):
            (entity_type, distance, info) = get_the_radar_data(angle)

            if entity_type == "player":
                found = True
                target_type = types[entity_type]
                target_distance = vector_to_components(distance, angle)
                target_angle = angle
                target_info = info
                break

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target_type = "\x00"
            target_distance = (0, 0)
            target_angle = 0

    # If we should still scan around us
    if not target_type == types["player"]:
        # Do a 360 degrees scan in a random quadrant
        for angle in range(0, 359):
            (entity_type, distance, info) = get_the_radar_data(angle)

            # Scan for our target without any priority.
            if entity_type == "player":
                target_type = types[entity_type]
                target_distance = vector_to_components(distance, angle)
                target_angle = angle
                target_info = info
                break

    return target_type, target_distance, target_angle, target_info


def scan_for_weapon(values, debug_circles):
    """
    Scans the play area for the target using its last known coordinates and making sure the found target is the closest
    to the player. It uses a three pass scan to find the target. First, it checks around the last known position to find
    the target again, making sure to always follow the target as long as nothing gets in the way. The second scan looks
    in a 90 degrees area around the target last known position in case it went faster. The third scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param debug_circles: An array to add any circle info for debugging. Will add a tuple with the target distance
    and the scan circle.
    :return: The information o
    :return: The information on the main target in four variables
    """
    target_type = "\x00"
    target_distance = (0, 0)
    target_angle = 0
    target_info = 0

    # Check if we have a targeted main target for scanning
    if values[3] != "\x00\x00" and values[4] != "\x00\x00":
        target_type = values[3][:1]
        target_angle = ord(values[3][1:])
        target_distance = (
            ord(values[4][:1]) - arena_dimensions[0],
            ord(values[4][1:]) - arena_dimensions[1],
        )

    if get_if_have_weapon():
        return target_type, target_distance, target_angle, target_info

    if target_type == types["weapon"]:
        debug_circles.append((target_distance, small_scan_range))

        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in angle_range(target_angle, small_scan_range):
            (entity_type, distance, info) = get_the_radar_data(angle)

            if entity_type == "weapon" and not info:
                found = True
                target_type = types[entity_type]
                target_distance = vector_to_components(distance, angle)
                target_angle = angle
                target_info = info
                break

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target_type = "\x00"
            target_distance = (0, 0)
            target_angle = 0

    # If we should still scan around us
    if not target_type == types["weapon"]:
        # Do a 360 degrees scan in a random quadrant
        possibility = None
        for angle in range(0, 359):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if possibility is None and entity_type == "weapon" and not info:
                possibility = (
                    entity_type,
                    distance_compo,
                    angle,
                    info,
                )
            elif possibility is not None and entity_type == "weapon"\
                    and compare_distance(distance_compo, possibility[1]) and not info:
                possibility = (
                    entity_type,
                    distance_compo,
                    angle,
                    info,
                )

        if possibility is not None and possibility[0] == "weapon":
            target_type = types[possibility[0]]
            target_distance = possibility[1]
            target_angle = possibility[2]
            target_info = possibility[3]

    return target_type, target_distance, target_angle, target_info


def scan_for_column(values, debug_circles):
    """
    Scans the play area for the target using its last known coordinates.
    It uses a two pass scan to find the target. First, it checks around the last known position to find the
    target again, making sure to always follow the target as long as nothing gets in the way. The second scan
    chooses a random quadrant of the map and looks there.
    :param values: The values saved inside the agent's data
    :param debug_circles: An array to add any circle info for debugging. Will add a tuple with the target distance
    and the scan circle.
    :return: The information on the main target in four variables
    """
    target_type = "\x00"
    target_distance = (0, 0)
    target_angle = 0
    target_info = 0

    # Check if we have a targeted main target for scanning
    if values[3] != "\x00\x00" and values[4] != "\x00\x00":
        target_type = values[3][:1]
        target_angle = ord(values[3][1:])
        target_distance = (
            ord(values[4][:1]) - arena_dimensions[0],
            ord(values[4][1:]) - arena_dimensions[1],
        )

    if target_type == types["column"]:
        debug_circles.append((target_distance, small_scan_range))

        # Scan in the vicinity of the main_target last known position
        found = False
        for angle in angle_range(target_angle, small_scan_range):
            (entity_type, distance, info) = get_the_radar_data(angle)

            if entity_type == "column":
                found = True
                target_type = types[entity_type]
                target_distance = vector_to_components(distance, angle)
                target_angle = angle
                target_info = info
                break

        # If we still couldn't find the main target, we lost it, reset that target
        if not found:
            target_type = "\x00"
            target_distance = (0, 0)
            target_angle = 0

    # If we should still scan around us
    if not target_type == types["column"]:
        # Do a 360 degrees scan in a random quadrant
        possibility = None
        for angle in range(0, 359):
            (entity_type, distance, info) = get_the_radar_data(angle)
            distance_compo = vector_to_components(distance, angle)

            if possibility is None and entity_type == "column":
                possibility = (
                    entity_type,
                    distance_compo,
                    angle,
                    info,
                )
            elif possibility is not None and entity_type == "column" \
                    and compare_distance(distance_compo, possibility[1]):
                possibility = (
                    entity_type,
                    distance_compo,
                    angle,
                    info,
                )

        if possibility is not None and possibility[0] == "column":
            target_type = types[possibility[0]]
            target_distance = possibility[1]
            target_angle = possibility[2]
            target_info = possibility[3]

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
        ), 0
    if position[1] - acceptable_distance < 0:
        return True, types["wall"], (
            0,
            -position[1],
        ), 270
    if position[1] + acceptable_distance > arena_dimensions[1]:
        return True, types["wall"], (
            0,
            arena_dimensions[1] - position[1],
        ), 90

    agent_angle = int(degrees(atan2(velocity[1], velocity[0])))

    for angle in angle_range(agent_angle, danger_scan_range):
        (entity_type, distance, info) = get_the_radar_data(angle)

        if (entity_type == "player" or entity_type == "column" or entity_type == "hazard")\
                and distance < acceptable_distance:
            return True, types[entity_type], vector_to_components(distance, angle), angle

        if entity_type == "weapon" and distance < acceptable_distance and info:
            return True, types[entity_type], vector_to_components(distance, angle), angle

    return False, "\x00", (0, 0), 0


def build_state_dict(position, dx, dy, rot_cc, rot_cw, current_state, target1_type, target1_distance, target1_angle,
                     target2_type, target2_distance, target2_angle, target3_type, target3_distance, target3_angle,
                     debug_circles):
    """
    Create the dictionary to send back to the game using the base info
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
    :param target3_type: The type of the third target
    :param target3_distance: The distance of the third target to the agent
    :param target3_angle: The angle of the third target from the agent.
    :param debug_circles: array of circles for debugging purposes, tuple of distance from player and the circle radius
    :return: A dictionary ready to be sent to the game
    """

    target1_distance1_char = "0"
    target1_distance2_char = "0"
    target1_angle_char = "0"
    try:
        target1_distance1_char = chr(int(arena_dimensions[0] + target1_distance[0]))
        target1_distance2_char = chr(int(arena_dimensions[1] + target1_distance[1]))
        target1_angle_char = chr(int(target1_angle))
    except ValueError:
        print("Broken data given to char for target 1 distance,", target1_distance, target1_angle, target1_type)

    target2_distance1_char = "0"
    target2_distance2_char = "0"
    target2_angle_char = "0"
    try:
        target2_distance1_char = chr(int(arena_dimensions[0] + target2_distance[0]))
        target2_distance2_char = chr(int(arena_dimensions[1] + target2_distance[1]))
        target2_angle_char = chr(int(target2_angle))
    except ValueError:
        print("Broken data given to char for target 2 distance,", target2_distance, target2_angle, target2_type)

    target3_distance1_char = "0"
    target3_distance2_char = "0"
    target3_angle_char = "0"
    try:
        target3_distance1_char = chr(int(arena_dimensions[0] + target3_distance[0]))
        target3_distance2_char = chr(int(arena_dimensions[1] + target3_distance[1]))
        target3_angle_char = chr(int(target3_angle))
    except ValueError:
        print("Broken data given to char for target 3 distance,", target3_distance, target3_angle, target3_type)

    debug = [
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
        (
            int(position[0]),
            int(position[1]),
            int(target3_distance[0] + position[0]),
            int(target3_distance[1] + position[1])
        ),
    ]

    for circle in debug_circles:
        debug.append((
            int(circle[0][0] + position[0]),
            int(circle[0][1] + position[1]),
            int(circle[1]),
        ))

    return {
        'ACLT_X': dx,
        'ACLT_Y': dy,
        'ROT_CC': rot_cc,
        'ROT_CW': rot_cw,
        'SAVE_A': states[current_state],
        'SAVE_B': target1_type + target1_angle_char,
        'SAVE_C': target1_distance1_char + target1_distance2_char,
        'SAVE_D': target2_type + target2_angle_char,
        'SAVE_E': target2_distance1_char + target2_distance2_char,
        'SAVE_F': target3_type + target3_angle_char,
        'SAVE_X': target3_distance1_char + target3_distance2_char,
        # Write debug lines to the found player and weapon
        'DEBUGS': debug
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


def invert_angle(angle):
    new_angle = angle - 180
    if new_angle < 0:
        new_angle = 359 + new_angle
    return new_angle


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


def empty_tuple(to_check):
    """
    Check if the tuple is empty by checking if both it's component are == 0
    :param to_check: The tuple to check
    :return: Whether or not that tuple is empty
    """
    return to_check[0] == 0 and to_check[1] == 0
