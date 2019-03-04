# -> CLASS DEMO

# This agent, as demonstrated in class, contains exactly three states. The first state describes the behaviour while
# it is looking for a weapon (since, at the beginning of the match, the player will be unequipped). The agent will
# transition out of this state only if it gains possession of a weapon, so until it has a weapon it will scan all 360
# degrees around its current position (in one degree increments) and, whenever a weapon is detected, it place the angle
# at which that weapon was detected and the distance to that weapon in a list of possible weapons to pursue. If there
# is at least one candidate weapon, the list of possibilities is sorted by distance so that the ACLT_X and ACLT_Y keys
# of the return dictionary can be set to a unit vector corresponding to the direction of the nearest weapon. If there
# are no weapons visible to the player, the ACLT_X and ACLT_Y values are randomized with a probability of 0.1, which
# essentially means that the player starts to wander around, changing direction randomly about every 10 frames. Whether
# a weapon is currently visible or not, the WEAPON value in the dictionary is always set to True so that the agent will
# pick up a weapon whenever possible. The second state describes the behaviour while the agent is looking for a target
# (since the only way into this state is through the acquisition of a weapon). If again requires scanning at all angles
# from the current location and, if the opposing player is not detected, move randomly. But if, on the other hand, the
# opposing player is detected, the agent will move in the direction of that player until they arrive within a distance
# of 200 units. Only when the player is within 200 units does the agent move into the third and final behaviour state.
# The third state, only entered when the player has a weapon and is within 200 units of the opponent, entails scanning
# all 360 degrees (again) for the opposing player, and comparing the angle at which the opposing player is visible 
# against the current throwing angle of the player. Using either the cross product (as discussed in class) or a branch
# structure such as the one demonstrated below, the player can decide whether it is faster to rotate clockwise or
# counterclockwise (updating the return dictionary accordingly). When the throwing angle nearly matches the angle at
# which the opposing player was seen, the weapon is thrown (by setting the WEAPON key value in the return dictionary\
# to false, and the machine returns to its first state and begins looking for another weapon.


# n.b., This agent has been deliberately designed to be rudimentary and somewhat inferior - constantly checking all 
# 360 degrees around the player is inefficient and does incur a cost (i.e., the main program will give your program
# less frames for consideration as a result), and checking in 1 degree increments results in many possible blind spots.
# Additionally, the manner in which certain objectives are achieved (i.e., finding the nearest weapon, deciding whether
# to turn clockwise or counterclockwise, attempting to reduce velocity, etc.) are not accomplished in the best manner.

# You should treat this CLASS DEMO agent as a starting point that allows you to observe "HOW" glad_AI_tors is played.



# the "start" function is REQUIRED by glad_AI_tors and must return your desired initial state and an empty dictionary

def start():
	return "look_for_weapon", {}

	
	
# the look_for_weapon function describes the behaviour when the agent is searching for (i.e., moving towards or wandering
# in search of) a weapon that it will use to against the opposing player

def look_for_weapon():

	# transition to the "next" state once you have a weapon
	if get_if_have_weapon():

		return "look_for_target", {"ACLT_X" : 0, "ACLT_Y" : 0}
		
	else:
	
		# search all 360 degrees for anything of type weapon
		possibilities = []
		for angle in range(0, 360, 1):
		
			(type, distance, _) = get_the_radar_data(angle)
			
			if type == 'weapon':
				possibilities.append( (distance, angle) )
		
		# if there were no visible weapons, "wander" around while remaining in the look_for_weapon state
		if len(possibilities) == 0:
			if randint(1, 10) == 1:
				return "look_for_weapon", {"WEAPON" : True, "ACLT_X" : randint(-1, 1), "ACLT_Y" : randint(-1, 1)}
			else:
				return "look_for_weapon", {"WEAPON" : True}
		
		# if there was at least one visible weapon, move in the direction of the closest one
		else:
			possibilities.sort()
			angle = possibilities[0][1]
			return "look_for_weapon", {"WEAPON" : True, "ACLT_X" : (cos(radians(angle))), "ACLT_Y" : (sin(radians(angle)))}
	
	
	
# the look_for_target function describes the behaviour when the agent has acquired a weapon and is now searching for (i.e.,
# moving towards or wandering in search of) the opposing player	

def look_for_target():

	# search all 360 degrees for the other player
	for angle in range(0, 360, 1):
	
		(type, distance, _) = get_the_radar_data(angle)

		# if the other player is visible...
		if type == 'player':
		
			# ...and within 200 units, move to the aiming state
			if distance < 200:
				return "aim_at_target", {"ACLT_X" : 0, "ACLT_Y": 0}
			
			# ...but if the player is still too far away, move in the direction of the opponent
			else:
				return "look_for_target", {"ACLT_X" : (cos(radians(angle))), "ACLT_Y" : (sin(radians(angle)))}

	# if the other player is not visible, "wander" around
	if randint(1, 10) == 1:
		return "look_for_target", {"ACLT_X" : randint(-1, 1), "ACLT_Y" : randint(-1, 1)}
	else:
		return "look_for_target", {}
	
	

# the aim_at_target function descibes the behaviour when the player has a weapon and is close enough to the opposing player
# (i.e., withing 200 units of distance) to rotate the throwing angle towards the opponent and attempt a shot
	
def aim_at_target():

	# search all 360 degrees for the other player
	for angle in range(0, 360, 1):
	
		(type, distance, _) = get_the_radar_data(angle)
		
		# if the other player is visible...
		if type == 'player':

			# ...get your current angle and compare it with the desired angle
			throw = get_throwing_angle()
			delta = ((angle - throw) + 360) % 360
			
			# if your current angle is almost the same as the desired angle, take the shot
			if delta < 1 or delta > 359:
			
				return "look_for_weapon", {"WEAPON" : False}
				
			# otherwise, decide whether to turn clockwise or counterclockwise
			elif delta > 180:
				rot_cc = 0
				rot_cw = 1
			else:
				rot_cc = 1
				rot_cw = 0
				
			return "aim_at_target", {"ROT_CC": rot_cc,  "ROT_CW": rot_cw}

	# if the other player is not visible, go back to the look_for_target state (presumably to wander around again)
	return "look_for_target", {}
