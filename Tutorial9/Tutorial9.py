import sys
import pygame
from Game import Game

screen_width = 910
screen_height = 950
frame_rate = 60


def main():
    pygame.init()
    clock = pygame.time.Clock()
    pygame.display.set_caption('Tower Builder')
    pygame.key.set_repeat(1, 1)

    game_instance = Game((screen_width, screen_height))
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
        pygame.display.flip()

        # Make sure we keep a consistent framerate
        clock.tick(frame_rate)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
