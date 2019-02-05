import pygame
import random


class Game:
    screen_width = 1024
    screen_height = 768
    framerate = 60

    base_asteroid_speed = 1
    max_velocity = 5
    asteroid_count = 8

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    def __init__(self):
        self.is_running = False
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.init()
        pygame.display.flip()
        pygame.key.set_repeat(1, 1)

        self.ship = {
            "position": (self.screen_width / 2, self.screen_height / 2),
            "velocity": (0, 0),
            "size": [30, 30],
            "angle": 0,
            "entity": None,
            "destroy": False,
        }

        self.asteroids = []
        for i in range(1, 8):
            self.asteroids.append({
                "position": (random.randint(50, self.screen_width - 50), random.randint(50, self.screen_height - 50)),
                "velocity": (
                    random.randint(self.base_asteroid_speed, self.max_velocity),
                    random.randint(self.base_asteroid_speed, self.max_velocity)
                ),
                "size": [50, 50],
                "entity": None,
            })

    def start(self):
        self.is_running = True

    def handle_input(self):
        # handle game input
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.handle_key_left()

                elif event.key == pygame.K_RIGHT:
                    self.handle_key_right()

                elif event.key == pygame.K_UP:
                    self.handle_key_up()

                elif event.key == pygame.K_DOWN:
                    self.handle_key_down()

                elif event.key == pygame.K_SPACE:
                    self.handle_key_space()

    def handle_key_left(self):
        self.ship['velocity'] = (
            self.ship['velocity'][0] - 1 if self.ship['velocity'][0] > -self.max_velocity else -self.max_velocity,
            self.ship['velocity'][1]
        )
        return

    def handle_key_right(self):
        self.ship['velocity'] = (
            self.ship['velocity'][0] + 1 if self.ship['velocity'][0] <= self.max_velocity else self.max_velocity,
            self.ship['velocity'][1]
        )
        return

    def handle_key_up(self):
        self.ship['velocity'] = (
            self.ship['velocity'][0],
            self.ship['velocity'][1] - 1 if self.ship['velocity'][0] > -self.max_velocity else -self.max_velocity
        )
        return

    def handle_key_down(self):
        self.ship['velocity'] = (
            self.ship['velocity'][0],
            self.ship['velocity'][1] + 1 if self.ship['velocity'][0] <= self.max_velocity else self.max_velocity,
        )
        return

    def handle_key_space(self):
        self.ship['fire'] = True
        return

    def render(self):
        self.screen.fill(self.BLACK)
        for asteroid in self.asteroids:
            pygame.draw.rect(self.screen, self.WHITE, (
                asteroid["position"][0],
                asteroid["position"][1],
                asteroid["size"][0],
                asteroid["size"][1],
            ))
        pygame.draw.rect(self.screen, self.WHITE, (
            self.ship["position"][0],
            self.ship["position"][1],
            self.ship["size"][0],
            self.ship["size"][1],
        ))
        return

    def update(self):
        # Update content
        for asteroid in self.asteroids:
            current_rect = pygame.Rect(
                asteroid["position"][0],
                asteroid["position"][1],
                asteroid["size"][0],
                asteroid["size"][1],
            )

            # If the asteroid is hitting the sides
            if asteroid["position"][0] <= 0 or asteroid["position"][0] + asteroid["size"][0] > self.screen_width:
                asteroid["velocity"] = (
                    -asteroid["velocity"][0],
                    asteroid["velocity"][1],
                )
            # If the asteroid is hitting the sides
            if asteroid["position"][1] <= 0 or asteroid["position"][1] + asteroid["size"][1] > self.screen_height:
                asteroid["velocity"] = (
                    asteroid["velocity"][0],
                    -asteroid["velocity"][1],
                )

            # check if the asteroid is hitting another asteroid
            for sub_asteroid in self.asteroids:
                # Ignore if this is the same asteroid
                if sub_asteroid["position"] == asteroid["position"][0]:
                    continue
                sub_rect = pygame.Rect(
                    sub_asteroid["position"][0],
                    sub_asteroid["position"][1],
                    sub_asteroid["size"][0],
                    sub_asteroid["size"][1],
                )

                if sub_rect.colliderect(current_rect):
                    # If the two asteroids collides, invert their velocities
                    temp_velocity = (
                        asteroid["velocity"][0],
                        asteroid["velocity"][1],
                    )
                    asteroid["velocity"] = (
                        sub_asteroid["velocity"][0],
                        sub_asteroid["velocity"][1],
                    )
                    sub_asteroid["velocity"] = (
                        temp_velocity[0],
                        temp_velocity[1],
                    )

            # Update the position with the velocity
            asteroid["position"] = (
                asteroid["position"][0] + asteroid["velocity"][0],
                asteroid["position"][1] + asteroid["velocity"][1],
            )

            # Check if that asteroid hit the ship
            ship_rect = pygame.Rect(
                self.ship["position"][0],
                self.ship["position"][1],
                self.ship["size"][0],
                self.ship["size"][1],
            )
            if sub_rect.colliderect(current_rect):
                self.ship["destroyed"] = True

        # If the ship is not hitting the sides
        if self.ship["position"][0] > 0 or self.ship["position"][0] + self.ship["size"][0] <= self.screen_width or\
           self.ship["position"][1] > 0 or self.ship["position"][1] + self.ship["size"][1] <= self.screen_height:
            self.ship["position"] = (
                self.ship["position"][0] + self.ship["velocity"][0],
                self.ship["position"][1] + self.ship["velocity"][1],
            )

        return

    def clean(self):
        # Clean content state for deletion
        return

    def end_game(self):
        self.is_running = False
