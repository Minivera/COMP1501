import sys
import pygame
from game.Game import Game

screen_width = 1024
screen_height = 768
frame_rate = 60


def main():
    clock = pygame.time.Clock()

    game_instance = Game((screen_width, screen_height))
    game_instance.start()

    all_sprites = pygame.sprite.Group()

    while game_instance.is_running:
        # Process game events
        game_instance.handle_input()

        # Render the game
        game_instance.update()
        game_instance.render(all_sprites)
        game_instance.clean()

        # Update display
        pygame.display.update()

        # Make sure we keep a consistent framerate
        clock.tick(frame_rate)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
