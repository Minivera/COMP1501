import game.States
from states.State import State
from states.MenuState import MenuState
from states.TutorialState import TutorialState
from states.GameState import GameState


class StateMachine:
    def __init__(self, initial_state):
        self.is_running = False
        self.state = initial_state
        self.state_instance = self.__get_state_instance()

    def change_state(self, new_state):
        self.state = new_state
        self.state_instance = self.__get_state_instance()

    def __get_state_instance(self):
        if self.state == game.States.STATE_MENU:
            return MenuState()
        if self.state == game.States.STATE_TUTORIAL:
            return TutorialState()
        if self.state == game.States.STATE_GAME:
            return GameState()
        return State()
