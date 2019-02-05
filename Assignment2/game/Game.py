import pygame
import game.States
from game.StateMachine import StateMachine


class Game:
    def __init__(self, screen_size):
        self.is_running = False
        self.state_machine = StateMachine(game.States.STATE_WAITING)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.init()
        pygame.display.set_caption('Awkward Dungeons')
        pygame.display.flip()
        pygame.key.set_repeat(1, 1)

    def start(self):
        self.state_machine = StateMachine(game.States.STATE_MENU)
        self.is_running = True

    def handle_input(self):
        # handle game input
        self.state_machine.state_instance.handle_input(self)

    def render(self, sprites):
        # render stuff
        self.state_machine.state_instance.render(self, sprites)
        sprites.draw(self.screen)

    def update(self):
        # Update content
        self.state_machine.state_instance.update(self)

    def clean(self):
        # Clean content state for deletion
        self.state_machine.state_instance.clean(self)

    def change_state(self, new_state):
        self.state_machine.change_state(new_state)

    def end_game(self):
        self.is_running = False
