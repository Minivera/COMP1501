import sys
import pygame
from Game import Game


def main():
    clock = pygame.time.Clock()

    game_instance = Game()
    game_instance.start()

    while game_instance.is_running:
        # Process game events
        game_instance.handle_input()

        # Render the game
        game_instance.update()
        game_instance.render()
        game_instance.clean()

        # Update display
        pygame.display.update()

        # Make sure we keep a consistent framerate
        clock.tick(game_instance.framerate)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
