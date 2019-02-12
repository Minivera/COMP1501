import pygame
import random
import sys
import math
import time
import os

# import the pygame constants (specifically the key codes and event types)
from pygame.locals import *

# constants for accessing the attributes of the mouse
MOUSE_LMB = 0
MOUSE_RMB = 1
MOUSE_X   = 2
MOUSE_Y   = 3

# the resolution of the display window (but please note that the toy runs in fullscreen mode)
window_wid = 640
window_hgt = 480

# the frame rate is the number of frames per second that will be displayed and although
# we could (and should) measure the amount of time elapsed, for the sake of simplicity
# we will make the (not unreasonable) assumption that this "delta time" is always 1/fps
frame_rate = 30
delta_time = 1 / frame_rate

# these are the colours through which the game objects can be "cycled"
included_colours = []
included_colours.append(Color(0, 0, 255))
included_colours.append(Color(0, 255, 0))
included_colours.append(Color(0, 255, 255))
included_colours.append(Color(255, 0, 0))
included_colours.append(Color(255, 0, 255))
included_colours.append(Color(255, 255, 0))

# these are the unique identifiers for the game objects
object_unique_id = 1000

# this is the only game object included in the "toy" - rename it when5 you decide what
# these objects will represent within the "magic circle" of your final game submission
# and feel free to modify it as required, as long as you preserve the core mechanics 
class Object:

    def __init__(self):

        # get the next unique identifier and increment
        global object_unique_id
        self.id = object_unique_id
        object_unique_id += 1

        # the radius of the game object is fixed
        self.radius = 20

        # the initial colour is randomly selected and the "focus" flag is false
        self.colour = random.randint(0, len(included_colours) - 1)
        self.flag = False

        # (x, y) / (dx, dy) / (ddx, ddy) is the position / velocity / acceleration
        self.x = random.randint(self.radius, window_wid - 1 - self.radius)
        self.y = random.randint(self.radius, window_hgt - 1 - self.radius)
        angle = random.randint(0, 359)
        self.dx = math.cos(math.radians(angle)) * 0.5
        self.dy = math.sin(math.radians(angle))	* 0.5
        self.ddx = 0
        self.ddy = 0


def get_all_inputs():

    # get the state of the mouse (i.e., button states and pointer position)
    mouse_dict = {}
    (mouse_dict[MOUSE_LMB], _, mouse_dict[MOUSE_RMB]) = pygame.mouse.get_pressed()
    (mouse_dict[MOUSE_X], mouse_dict[MOUSE_Y]) = pygame.mouse.get_pos()

    # get the state of the keyboard
    keybd_tupl = pygame.key.get_pressed()

    # look in the event queue for the quit event
    quit_ocrd = False
    for evnt in pygame.event.get():
        if evnt.type == QUIT:
            quit_ocrd = True

    # return all possible inputs
    return mouse_dict, keybd_tupl, quit_ocrd


def update_all_game_objects(game_objects, mouse_dict):

    # visit all the game objects...
    for object in game_objects:

        # reset the flags
        object.flag = False

        # if the game object is beneath the mouse...
        if ((object.x - mouse_dict[MOUSE_X]) ** 2 + (object.y - mouse_dict[MOUSE_Y]) ** 2) < (object.radius ** 2):

            # ...then set the flag on that one
            object.flag = True

            # if the left button is clicked, change the colour
            if mouse_dict[MOUSE_LMB]:

                object.colour = (object.colour + 1) % len(included_colours)

            # if the right button is clicked, attract all other objects of the same colour
            elif mouse_dict[MOUSE_RMB]:

                for another in game_objects:

                    if another.id != object.id and another.colour == object.colour:

                        delta_x = object.x - another.x
                        delta_y = object.y - another.y
                        magnitude = math.sqrt(delta_x ** 2 + delta_y ** 2)

                        another.dx = another.dx + (delta_x / magnitude) / 2
                        another.dy = another.dy + (delta_y / magnitude) / 2

        # update the positions
        object.x += object.dx
        object.y += object.dy

    return game_objects


def main():

    # initialize pygame
    pygame.init()

    # create the window and set the caption of the window
    window_sfc = pygame.display.set_mode( (window_wid, window_hgt) ) #, FULLSCREEN )
    pygame.display.set_caption('Include the Name for Your Submission Here')

    # create a clock
    clock = pygame.time.Clock()

    number_of_objects = 10
    game_objects = []
    for i in range(number_of_objects):
        game_objects.append(Object())

    # the game loop is a postcondition loop controlled using a Boolean flag
    closed_flag = False
    while not closed_flag:

        # get the inputs from the mouse and check if the window has been closed
        mouse_dict, keybd_tupl, closed_flag = get_all_inputs()
        if keybd_tupl[pygame.K_ESCAPE]:
            closed_flag = True

        # update the positions and velocities of all the game objects in the toy
        game_objects = update_all_game_objects(game_objects, mouse_dict)

        # render the game objects to the display
        window_sfc.fill(Color(255, 255, 255))

        # draw each of the game objects and encircle the one that is flagged
        for object in game_objects:

            pygame.draw.circle(window_sfc, included_colours[object.colour], (int(object.x), int(object.y)), object.radius)

            if object.flag:
                pygame.draw.circle(window_sfc, Color(0, 0, 0), (int(object.x), int(object.y)), object.radius + 5, 2)

        # update the display and enforce the minimum frame rate
        pygame.display.update()
        clock.tick(frame_rate)


if __name__ == "__main__":
    main()
