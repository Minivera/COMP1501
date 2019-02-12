import pygame


class State:
    def handle_input(self, game):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game.end_game()
                return
        return

    def render(self, game, sprites):
        # render stuff
        return

    def update(self, game):
        # Update content
        return

    def clean(self, game):
        # Clean content state for deletion
        return
