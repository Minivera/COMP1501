import pygame
import random
from entities.Ball import Ball
from entities.Grog import Grog
from entities.ScoreBoard import ScoreBoard
from entities.Menu import Menu
from entities.Colours import possible_colours, next_color

STATE_NONE = -1
STATE_MENU = 0
STATE_GAME = 1

BUTTON_LEFT = 1
BUTTON_RIGHT = 3


class Game:
    max_number_of_balls = 15

    size_steps = [0.40, 0.50, 0.60, 0.80, 1]

    base_score = 2000

    score_loss = 100

    def __init__(self, screen_size):
        self.is_running = False
        self.state = STATE_NONE
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(screen_size)
        self.balls = []
        self.clicks_this_round = 0
        self.score = 0
        self.round_finished = False
        self.grog = Grog((screen_size[0], 200), (0, 0))
        self.score_board = ScoreBoard(self.score, (screen_size[0], 30), (0, screen_size[1] - 30))
        self.menu = Menu(screen_size, (0, 0))
        self.grog.determine_meal()
        self.target = None

    def generate_field(self):
        for demand in self.grog.requests:
            current = random.randint(1, max(1, demand["quantity"] // 2))
            count = 0
            while count < demand["quantity"]:
                count += current
                self.balls.append(
                    Ball(
                        demand["color"],
                        current,
                        0,
                        (
                            random.randint(Ball.base_radius, self.screen_size[0] - Ball.base_radius),
                            random.randint(Ball.base_radius + 200, self.screen_size[1] - Ball.base_radius - 30),
                        ),
                    )
                )
                current = random.randint(1, max(1, demand["quantity"] - count))
        return

    def add_balls(self):
        count = random.randint(len(self.balls) - 1, self.max_number_of_balls)
        for i in range (1, count):
            self.balls.append(
                Ball(
                    possible_colours[random.randint(0, len(possible_colours) - 1)],
                    random.randint(1, 3),
                    0,
                    (
                        random.randint(Ball.base_radius, self.screen_size[0] - Ball.base_radius),
                        random.randint(Ball.base_radius + 200, self.screen_size[1] - Ball.base_radius),
                    ),
                )
            )

    def start(self):
        self.state = STATE_MENU
        self.is_running = True

    def handle_input(self):
        # handle game input
        mouse_pos = pygame.mouse.get_pos()

        events = pygame.event.get()
        if self.state == STATE_MENU:
            # Only the events for the menu
            for event in events:
                if event.type == pygame.QUIT:
                    self.end_game()
                    return

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == BUTTON_LEFT and\
                            pygame.Rect(self.menu.button_rect).collidepoint(mouse_pos[0], mouse_pos[1]):
                        self.state = STATE_GAME
                        self.generate_field()
            return

        # Now manage the game if not is menu state
        ready = True
        for ball in self.balls:
            if ball.moving or ball.resizing:
                ready = False
                break

        self.grog.change_mouse_pos(mouse_pos)

        if ready:
            for ball in self.balls:
                ball.focused = False
                # Check if any ball is under the cursor
                if ((ball.position[0] - mouse_pos[0]) ** 2 + (ball.position[1] - mouse_pos[1]) ** 2)\
                        < (ball.current_radius ** 2):
                    ball.focused = True

        for event in events:
            if event.type == pygame.QUIT:
                self.end_game()
                return

            if ready and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.add_balls()
                    self.clicks_this_round += 5
                    continue

            if ready and event.type == pygame.MOUSEBUTTONUP:
                for ball in self.balls:
                    if event.button == BUTTON_LEFT:
                        if ((ball.position[0] - mouse_pos[0]) ** 2 + (ball.position[1] - mouse_pos[1]) ** 2) \
                                < (ball.current_radius ** 2):
                            ball.colour = next_color(ball.colour)
                            self.clicks_this_round += 1

                    if event.button == BUTTON_RIGHT:
                        if ((ball.position[0] - mouse_pos[0]) ** 2 + (ball.position[1] - mouse_pos[1]) ** 2) \
                                < (ball.current_radius ** 2):
                            self.target = ball
                            self.clicks_this_round += 1
        return

    def render(self, sprites):
        # render stuff
        self.screen.fill((0, 0, 0))

        if self.state == STATE_MENU:
            sprites.add(self.menu)

        if self.state == STATE_GAME:
            for ball in self.balls:
                if not ball.exists:
                    continue
                sprites.add(ball)

            sprites.add(self.grog)
            sprites.add(self.score_board)

        sprites.draw(self.screen)

    def update(self):
        if self.state == STATE_MENU:
            return

        if self.target is not None:
            for ball in self.balls:
                # Ignore the target or any ball not of the right type, but don't if the target is grog
                if not isinstance(self.target, Grog) and (ball == self.target or ball.colour != self.target.colour):
                    continue

                ball.seek_to(self.target)

        # Check for collisions
        current_highest = 0
        for ball in self.balls:
            # Ignore balls that don't exists
            if not ball.exists:
                continue

            # if the ball is the target, do nothing
            if self.target == ball:
                current_highest = max(current_highest, ball.number)
                continue

            # ignore the rest if grog is the target
            if self.target is not None and isinstance(self.target, Grog):
                # Check if the ball collides with Grog
                if pygame.Rect(self.target.rect).contains(pygame.Rect(ball.rect)):
                    ball.exists = False
                continue

            # Check if the ball collides with the ball target
            if self.target is not None and ball.collides_with(self.target):
                self.target.number = self.target.number + ball.number
                ball.exists = False
                continue

            for sub_ball in self.balls:
                # Ignore ourselves and dead balls
                if ball == sub_ball or not sub_ball.exists:
                    continue

                if ball.collides_with(sub_ball):
                    # If two ball collides, check if their type is the same
                    if ball.colour == sub_ball.colour:
                        # Give priority to the ball
                        ball.number = ball.number + sub_ball.number
                        sub_ball.exists = False
                    else:
                        # If they're not of the same type, reduce their numbers
                        temp = ball.number
                        ball.number = ball.number - sub_ball.number
                        sub_ball.number = sub_ball.number - temp
                        # Check if any of the two balls disappeared
                        ball.exists = ball.number > 0
                        sub_ball.exists = sub_ball.number > 0

            current_highest = max(current_highest, ball.number)

        # change all the ball's scales depending on the highest
        for ball in self.balls:
            # Ignore balls that do not exists
            if not ball.exists:
                continue

            # Check if at least a ball existed, if not, keep the last scale
            if current_highest > 0:
                ball.scale = self.size_steps[self.__get_scale(ball.number, current_highest)]

            ball.update()
        return

    def __get_scale(self, number, highest):
        count = len(self.size_steps)
        while highest >= 1:
            highest = highest - number
            count = max(0, count - 1)
        return count

    def clean(self):
        if self.state != STATE_MENU:
            self.menu.kill()
        else:
            # Don't clean anything when in the menu
            return

        # Clean content stated for deletion
        for i in range(len(self.balls) - 1, -1, -1):
            ball = self.balls[i]
            if not ball.exists:
                self.balls.pop(i)
                ball.kill()

        ready = True
        for ball in self.balls:
            if ball.moving or ball.resizing:
                ready = False
                break

        if ready:
            self.target = None
            if not self.round_finished and self.grog.demands_met(self.balls):
                self.round_finished = True
                self.target = self.grog

            if self.round_finished and len(self.balls) <= 0:
                # If the game finished and was cleaned, generate a new state
                self.determine_score()
                self.generate_field()
                self.grog.determine_meal()
                self.round_finished = False
                self.clicks_this_round = 0
        return

    def determine_score(self):
        self.score += max(self.base_score - self.score_loss * self.clicks_this_round, 0)
        self.score_board.change_score(self.score)
        return

    def end_game(self):
        self.is_running = False
