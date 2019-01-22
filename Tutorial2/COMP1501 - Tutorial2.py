#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

import pygame
import time
import random
import sys

walls = {
    'left': 0,
    'right': 800,
    'top': 0,
    'bottom': 800
}

circleRadius = 10
paddleWitdh = 200
paddleHeight = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#### ====================================================================================================================== ####
#############                                         INITIALIZE                                                   #############
#### ====================================================================================================================== ####

def initialize():
    ''' Central Initialize function. Calls helper functions to initialize Pygame and then the game_data dictionary.
    handle_input: None
    Output: game_data Dictionary
    '''
    screen = initialize_pygame()
    return initialize_data(screen)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def initialize_data(screen):
    ''' Initializes the game_data dictionary. Includes: Entity Data and Logistical Data (is_open).
    Input: pygame screen
    Output: game_data Dictionary
    '''
    # Initialize game_data Dictionary
    game_data = {"screen": screen,
                "entities":[],
                'is_open': True}
    entities = []
    
    # Generate 'Ball' Entities
    for i in range(random.randint(3, 6)):
        entities.append({'type': 'ball',
                         'location': [random.randint(10, 790), random.randint(10, 790)],
                         'velocity': [random.randint(5, 15), random.randint(5, 15)]})
        
    # Generate 'Paddle' Entity
    entities.append({'type': 'paddle',
                     'location': [300, 780],
                     'velocity': 9,
                     'size': [200, 20],
                     'color': (0, 0, 0),
                     'current_action': 'NA'})
    game_data["entities"] = entities
    return game_data

def initialize_pygame():
    ''' Initializes Pygame.
    Input: None
    Output: pygame screen
    '''
    pygame.init()
    pygame.key.set_repeat(1, 1)
    return pygame.display.set_mode((800, 800))

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
            if event.key == pygame.K_LEFT:
                handle_key_left(game_data)
            if event.key == pygame.K_RIGHT:
                handle_key_right(game_data)
            if event.key == pygame.K_ESCAPE:
                handle_key_escape(game_data)
            pass

#############                                           HANDLERS                                                   #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def handle_key_left(game_data):
    paddle = find_paddle(game_data)
    paddle['current_action'] = 'ML'
    return

def handle_key_right(game_data):
    paddle = find_paddle(game_data)
    paddle['current_action'] = 'MR'
    return

def handle_key_escape(game_data):
    sys.exit()
    return
    
#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####
    
def update(game_data):
    ''' Central Update function. Calls helper functions to update various types of Entities [ball, paddle].
    Input: game_data Dictionary
    Output: None
    '''
    for entity in game_data["entities"]:
        
        # Handle 'Ball' Entity
        if entity['type'] == 'ball':
            update_ball(entity)
            
        # Handle 'Paddle' Entity
        elif entity['type'] == 'paddle':
            update_paddle(entity)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def find_paddle(game_data):
    for entity in game_data["entities"]:
        if entity['type'] == 'paddle':
            return entity
    return


def update_ball(entity):
    # Handle collision with left wall
    if entity['location'][0] + entity['velocity'][0] <= walls['left']:
        entity['velocity'][0] = -entity['velocity'][0]
    # Handle collision with right wall
    if entity['location'][0] + entity['velocity'][0] >= walls['right'] - circleRadius:
        entity['velocity'][0] = -entity['velocity'][0]
    # Handle collision with top wall
    if entity['location'][1] + entity['velocity'][1] <= walls['top']:
        entity['velocity'][1] = -entity['velocity'][1]
    # Handle collision with bottom wall
    if entity['location'][1] + entity['velocity'][1] >= walls['bottom'] - circleRadius:
        entity['velocity'][1] = -entity['velocity'][1]
        
    entity['location'][0] += entity['velocity'][0]
    entity['location'][1] += entity['velocity'][1]
    return

def update_paddle(entity):
    ''' Updates the location of a given 'Paddle' Entity based on 'current_action' flag.
    Input: entity Dictionary
    Output: None
    '''
    # Handle No Movement
    if entity['current_action'] == 'NA':
        return
    
    if entity['current_action'] == 'ML' and entity['location'][0] - entity['velocity'] > walls['left']:
        entity['location'][0] -= entity['velocity']
    elif entity['current_action'] == 'MR' and entity['location'][0] + entity['velocity'] < walls['right'] - paddleWitdh:
        entity['location'][0] += entity['velocity']
        
    entity['current_action'] = 'NA'
    return

#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####

def render(game_data):
    ''' Central Render function. Calls helper functions to render various views.
    Input: game_data Dictionary
    Output: None
    '''
    render_raw_data(game_data)
    render_pygame(game_data)

#############                                           HELPERS                                                    #############
#### ---------------------------------------------------------------------------------------------------------------------- ####

def render_raw_data(game_data):
    ballIndex = 1
    strings = []
    for entity in game_data["entities"]:
        # Handle 'Ball' Entity
        if entity['type'] == 'ball':
            strings.append('ball_' + str(ballIndex) + ' (' + str(entity['location'][0]) + ', ' + str(entity['location'][1]) + ')')
            ballIndex += 1

        # Handle 'Paddle' Entity
        elif entity['type'] == 'paddle':
            strings.append('paddle' + ' (' + str(entity['location'][0]) + ', ' + str(entity['location'][1]) + ')')

    print(', '.join(strings))
    return

def render_pygame(game_data):
    game_data["screen"].fill(BLACK)

    for entity in game_data["entities"]:
        # Handle 'Ball' Entity
        if entity['type'] == 'ball':
            pygame.draw.circle(
                game_data["screen"],
                GREEN,
                (entity['location'][0] + circleRadius, entity['location'][1] + circleRadius),
                circleRadius
            )

        # Handle 'Paddle' Entity
        elif entity['type'] == 'paddle':
            pygame.draw.rect(
                game_data["screen"],
                RED,
                (entity['location'][0], entity['location'][1], paddleWitdh, paddleHeight)
            )

    pygame.display.update()
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
