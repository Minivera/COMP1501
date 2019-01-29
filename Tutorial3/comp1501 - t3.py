#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import pygame
import time
import random
import sys
import math

#### ====================================================================================================================== ####
#############                                         INITIALIZE                                                   #############
#### ====================================================================================================================== ####

screen_width = 1200
screen_height = 800
base_speed = 15
gravity = 0.18

def initialize():
    ''' Central Initialize function. Calls helper functions to initialize Pygame and then the game_data dictionary.
    Input: None
    Output: game_data Dictionary
    '''
    screen = initialize_pygame()
    return initialize_data(screen)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


def initialize_data(screen, num_cannon_balls=6, num_targets=1):
    ''' Initializes the game_data dictionary. Includes: Entity Data and Logistical Data (is_open).
    Input: pygame screen
    Output: game_data Dictionary
    '''
    # Initialize game_data Dictionary
    game_data = {
        "screen": screen,
        "background": pygame.transform.scale(pygame.image.load("resources/backgrounds/background.png").convert_alpha(), (screen_width, screen_height)),
        "entities": [],
        'is_open': True,
        "ammo": pygame.transform.scale(pygame.image.load("resources/cannonball/cannonball.png").convert_alpha(), (20,20)),
        "settings": {
            "max_targets": num_targets,
            "max_cannon_balls": num_cannon_balls
        }
    }

    # Initialize Target Object(s)
    for _ in range(num_targets):
        game_data["entities"].append({
            "type": "target",
            "location": [random.randint(100, 400), random.randint(200, 600)],
            "size": (150, 150),
            "sprite": pygame.transform.scale(pygame.image.load("resources/targets/target_{}.png".format(random.randint(1, 4))).convert_alpha(), (150, 150)),
            "is_hit": False,
            "life": random.randint(200, 600)
        })

    # Initialize CannonBall Object(s)
    for _ in range(num_cannon_balls):
        game_data["entities"].append({
            "type": "cannonball",
            "location": [1100, 750],
            "velocity": None,
            "size": (25,25),
            "sprite": pygame.transform.scale(pygame.image.load("resources/cannonball/cannonball.png").convert_alpha(), (25,25)),
            "exists": False,
            "destroy": False
        })


    # Initialize Cannon Object(s)
    game_data["entities"].append({
        "type": "cannon",
        "location": [1100, 675], # Note: When rotating, you may need to adjust the location to (1300, 875) depending on your method
        "size": (200, 150),
        "sprite": pygame.transform.scale(pygame.image.load("resources/cannons/cannon_{}.png".format(random.randint(1, 4))).convert_alpha(), (200, 150)),
        "loaded": True,
        "is_firing": False,
        "angle": 45.00,
        "is_moving": False,
        "power": 10
    })

    # Initialize CrossHair Object
    game_data["entities"].append({
        "type": "crosshair",
        "location": pygame.mouse.get_pos(),
        "size": (100, 100),
        "has_moving": False,
        "sprite": pygame.transform.scale(pygame.image.load("resources/crosshairs/crosshair_{}.png".format(random.randint(1, 4))).convert_alpha(), (100, 100))
    })
    
    return game_data


def initialize_pygame():
    ''' Initializes Pygame.
    Input: None
    Output: pygame screen
    '''
    pygame.init()
    pygame.key.set_repeat(1, 1)
    return pygame.display.set_mode((1200, 800))

#### ====================================================================================================================== ####
#############                                           handle_input                                                    #############
#### ====================================================================================================================== ####


def handle_input(game_data):
    ''' Central handle_input function. Calls helper functions to handle various KEYDOWN events.
    Input: game_data Dictionary
    Output: None
    '''
    events = pygame.event.get()
    for event in events:
        
        # Handle [x] Press
        if event.type == pygame.QUIT:
            game_data['is_open'] = False
            
        # Handle Key Presses
        if event.type == pygame.KEYDOWN:
                
            # Handle 'Escape' Key
            if event.key == pygame.K_ESCAPE:
                handle_key_escape(game_data)

        # Handle Mouse Movement
        if event.type == pygame.MOUSEMOTION:
            handle_mouse_movement(game_data)

        # Handle Mouse Click
        if event.type == pygame.MOUSEBUTTONUP:
            handle_mouse_click(game_data)

#############                                           HANDLERS                                                   #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


def handle_mouse_movement(game_data):
    mouse = pygame.mouse.get_pos()
    for entity in game_data["entities"]:
        if entity['type'] == 'crosshair' and entity['has_moving'] and entity['location'] == mouse:
            entity['has_moving'] = False
        elif entity['type'] == 'crosshair' and not entity['has_moving']:
            entity['has_moving'] = True
        elif entity['type'] == 'cannon':
            entity['is_moving'] = True
    return


def handle_mouse_click(game_data):
    for entity in game_data["entities"]:
        if entity['type'] == 'cannonball' and entity['exists'] == False:
            entity['exists'] = True
    return


def handle_key_escape(game_data):
    ''' Handles the Escape KEYDOWN event. Sets a flag for 'is_open' to 'False'.
    Input: game_data Dictionary
    Output: None
    '''
    game_data['is_open'] = False

#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####


def update(game_data):
    ''' Central Update function. Calls helper functions to update various types of Entities [crosshair, target, cannon, cannonball].
    Input: game_data Dictionary
    Output: None
    '''
    for entity in game_data["entities"]:
        if entity['type'] == 'crosshair' and entity['has_moving'] == True:
            update_cross_hair(entity)
        if entity['type'] == 'cannon' and entity['is_moving'] == True:
            update_cannon(entity)
        if entity['type'] == 'cannonball' and entity['exists'] == True:
            cannon_entity = None
            target_entity = None
            for more_entities in game_data["entities"]:
                if more_entities["type"] == "target":
                    target_entity = more_entities
                elif more_entities["type"] == "cannon":
                    cannon_entity = more_entities
            update_cannon_ball(entity, cannon_entity, target_entity)
        if entity['type'] == 'target':
            update_target(entity)
            

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


def update_cross_hair(entity):
    mouse = pygame.mouse.get_pos()
    entity['location'] = [mouse[0] - entity['size'][0] / 2, mouse[1] - entity['size'][1] / 2]
    return


def update_cannon(entity):
    mouse = pygame.mouse.get_pos()
    entity['angle'] = - (math.atan2(entity['location'][1] - mouse[1], entity['location'][0] - mouse[0])) * 180/math.pi + 270
    return


def update_cannon_ball(entity, cannon_entity, target_entity):
    if entity['destroy']:
        entity['velocity'] = None
        entity['location'] = cannon_entity['location']
        entity['destroy'] = False
        entity['exists'] = False
        return

    if entity['velocity'] is None:
        mouse = pygame.mouse.get_pos()
        angle = math.atan2(screen_height - mouse[1], screen_width - mouse[0])
        entity['velocity'] = (math.cos(angle) * base_speed, math.sin(angle) * base_speed)

    entity['velocity'] = (entity['velocity'][0], entity['velocity'][1] - gravity)
    entity['location'] = (entity['location'][0] - entity['velocity'][0], entity['location'][1] - entity['velocity'][1])

    if entity['location'][0] < 0 or entity['location'][1] >= screen_height or entity['location'][1] < 0:
        entity['destroy'] = True
        return

    entity_rect = pygame.Rect(entity['location'], entity['size'])
    target_rect = pygame.Rect(target_entity['location'], target_entity['size'])
    if entity_rect.colliderect(target_rect):
        entity['destroy'] = True
        target_entity['is_hit'] = True
        return
    return


def update_target(entity):
    entity['life'] -= 1

    if entity['life'] <= 0:
        entity['is_hit'] = True

    if entity['is_hit']:
        entity['location'] = [random.randint(100, 400), random.randint(200, 600)]
        entity['life'] = random.randint(200, 600)
        entity['is_hit'] = False
        return

    return

#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####


def render(game_data):
    ''' Central Render function. Calls helper functions to render various views.
    Input: game_data Dictionary
    Output: None
    '''
    game_data["screen"].blit(game_data["background"], (0, 0))
    
    for entity in game_data["entities"]:
        if entity['type'] == 'cannon':
            render_cannon(game_data, entity)
        elif entity['type'] == 'cannonball':
            render_cannon_ball(game_data, entity)
        elif entity['type'] == 'target':
            render_target(game_data, entity)
        elif entity['type'] == 'crosshair':
            render_crosshair(game_data, entity)
            
    pygame.display.flip()

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####


def render_target(game_data, entity):
    screen = game_data['screen']
    screen.blit(entity['sprite'], entity['location'])
    return


def render_crosshair(game_data, entity):
    screen = game_data['screen']
    screen.blit(entity['sprite'], entity['location'])
    return


def render_cannon(game_data, entity):
    screen = game_data['screen']
    rotated_sprite = pygame.transform.rotate(entity['sprite'], entity['angle'])

    # ensure that the center of the bounding rectangle on the rotated image
    # is at the same position as the center of the rectangle for the initial
    rotated_rect = rotated_sprite.get_rect(center=entity['location'])
    screen.blit(rotated_sprite, rotated_rect)
    return


def render_cannon_ball(game_data, entity):
    if not entity['exists']:
        return
    screen = game_data['screen']
    screen.blit(entity['sprite'], entity['location'])
    return


def render_ammo(game_data, ammo_list):
    ''' Replace this and the return statement with your code '''
    return

#### ====================================================================================================================== ####
#############                                             MAIN                                                     #############
#### ====================================================================================================================== ####


def main():
    ''' Main function of script - calls all central functions above via a Game Loop code structure.
    Input: None
    Output: None
    '''
    # Initialize Data and Pygame
    game_data = initialize()
    
    # Begin Central Game Loop
    while game_data['is_open']:
        handle_input(game_data)
        update(game_data)
        render(game_data)
        time.sleep(0.01) # Small Time delay to slow down frames per second
        
    # Exit Pygame and Python
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
