"""----------------------------------------------------------------------------
TITLE       : main.py
BY          : Fairybytes
DESCRIPTION : Snake Game
REFERENCES  : None
----------------------------------------------------------------------------"""

# Import modules
import pygame
import random

"""----------------------------------------------------------------------------

0. SET UP SURFACE

----------------------------------------------------------------------------"""

pygame.font.init()
pygame.mixer.init()

# Set screen size
WIDTH, HEIGHT = 500, 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Set border
BORDER = pygame.Rect(0, 0, WIDTH, 50)

# Set font
SCORE_FONT = pygame.font.SysFont('arial', 20)
WINNER_FONT = pygame.font.SysFont('arial', 60)
DEAD_FONT = pygame.font.SysFont('arial', 60)

# Set screen title
pygame.display.set_caption("Fairybytes: Snake Game")

# Set colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Set constants
FPS = 15
VEL = 10
S_WIDTH = 10
S_HEIGHT = 10
S_START_POS_X = WIDTH // 2
S_START_POS_Y = (HEIGHT + 50) // 2
A_WIDTH = 10
A_HEIGHT = 10


def draw_window(HEAD, BODY, APPLE, snake_score):

    # Redraw background
    pygame.draw.rect(WIN, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT))

    # Redraw snake
    pygame.draw.rect(WIN, WHITE, HEAD)

    for body in BODY:
        pygame.draw.rect(WIN, GREEN, body)

    # Draw apple
    pygame.draw.rect(WIN, RED, APPLE)

    # Draw border
    pygame.draw.rect(WIN, WHITE, BORDER)

    # Write score at top left
    score_text = SCORE_FONT.render(
        "Score: " + str(snake_score),
        1,
        BLACK
    )

    WIN.blit(score_text, (10, 12))

    # If user reaches score of 15
    if snake_score == 15:
        winner_text = WINNER_FONT.render("You won!", 1, WHITE)
        WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width() /
                               2, HEIGHT/2 - winner_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(3000)
        return False

    # Collide with wall
    if HEAD.x < 0 or HEAD.x > WIDTH - S_WIDTH or HEAD.y < 50 or HEAD.y > HEIGHT - S_HEIGHT:
        dead_text = DEAD_FONT.render("GAME OVER", 1, WHITE)

        WIN.blit(dead_text, (WIDTH/2 - dead_text.get_width() /
                             2, HEIGHT/2 - dead_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(3000)
        return False

    # Collide with self
    if HEAD in BODY:
        dead_text = DEAD_FONT.render("GAME OVER", 1, WHITE)

        WIN.blit(dead_text, (WIDTH/2 - dead_text.get_width() /
                             2, HEIGHT/2 - dead_text.get_height()/2))

        pygame.display.update()
        pygame.time.delay(3000)
        return False

    return True


def genet_apple(head, body):

    snake_x = [head.x]
    for b in body:
        snake_x.append(b.x)

    snake_y = [head.y]
    for b in body:
        snake_y.append(b.y)

    while True:
        apple_x = random.randrange(0, WIDTH - A_WIDTH + 1, 10)

        if apple_x not in snake_x:
            apple_y = random.randrange(50, HEIGHT - A_HEIGHT + 1, 10)

            if apple_y not in snake_y:
                break

    APPLE = pygame.Rect(apple_x, apple_y, A_WIDTH, A_HEIGHT)
    return APPLE


def snake_bodymove(head, body, eaten):

    if eaten:

        # Append the last body into BODY
        body.append(body[-1])

        # Update BODY
        # each body gets the rect property of the previous body
        for i in range(len(body)-2, 0, -1):
            body[i] = body[i-1]
        body[0] = head

    else:
        # Update BODY
        # each body gets the rect property of the previous body
        for i in range(len(body)-1, 0, -1):
            body[i] = body[i-1]
        body[0] = head

    return body


"""----------------------------------------------------------------------------
                                    MAIN
----------------------------------------------------------------------------"""


def main():

    # Initialize HEAD
    HEAD = pygame.Rect(S_START_POS_X, S_START_POS_Y, S_WIDTH, S_HEIGHT)

    # Initialize BODY
    BODY = [
        pygame.Rect(S_START_POS_X, S_START_POS_Y - 10, S_WIDTH, S_HEIGHT),
        pygame.Rect(S_START_POS_X, S_START_POS_Y - 20, S_WIDTH, S_HEIGHT),
        pygame.Rect(S_START_POS_X, S_START_POS_Y - 30, S_WIDTH, S_HEIGHT)
    ]

    # Initialize APPLE
    APPLE = genet_apple(HEAD, BODY)

    # Check if apple eaten?
    eaten_status = False

    # Initialize score and snake direction
    snake_score = 0
    snake_direction = "RIGHT"

    # Set clock and FPS
    clock = pygame.time.Clock()

    running = True

    while running:

        clock.tick(FPS)

        # Check every individual event from user
        for event in pygame.event.get():

            # IF USER QUITS
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

            # IF USER USES KEYS
            if event.type == pygame.KEYDOWN:

                # KEY: UP
                if event.key == pygame.K_UP and snake_direction is not "DOWN":
                    snake_direction = "UP"

                # KEY: DOWN
                if event.key == pygame.K_DOWN and snake_direction is not "UP":
                    snake_direction = "DOWN"

                # KEY: LEFT
                if event.key == pygame.K_LEFT and snake_direction is not "RIGHT":
                    snake_direction = "LEFT"

                # KEY: RIGTH
                if event.key == pygame.K_RIGHT and snake_direction is not "LEFT":
                    snake_direction = "RIGHT"

        if APPLE.x == HEAD.x and APPLE.y == HEAD.y:
            eaten_status = True
            snake_score += 1

        if snake_direction == 'UP':

            # 1. Update BODY
            # each body gets the rect property of the previous body
            BODY = snake_bodymove(HEAD, BODY, eaten_status)

            # 2. Update HEAD
            HEAD = pygame.Rect(
                HEAD.x, HEAD.y - VEL,
                S_WIDTH, S_HEIGHT
            )

        if snake_direction == 'DOWN':

            # 1. Update BODY
            # each body gets the rect property of the previous body
            BODY = snake_bodymove(HEAD, BODY, eaten_status)

            # 2. Update HEAD
            HEAD = pygame.Rect(
                HEAD.x, HEAD.y + VEL,
                S_WIDTH, S_HEIGHT
            )

        if snake_direction == 'LEFT':

            # 1. Update BODY
            # each body gets the rect property of the previous body
            BODY = snake_bodymove(HEAD, BODY, eaten_status)

            # 2. Update HEAD
            HEAD = pygame.Rect(
                HEAD.x - VEL, HEAD.y,
                S_WIDTH, S_HEIGHT
            )

        if snake_direction == 'RIGHT':

            # 1. Update BODY
            # each body gets the rect property of the previous body
            BODY = snake_bodymove(HEAD, BODY, eaten_status)

            # 2. Update HEAD
            HEAD = pygame.Rect(
                HEAD.x + VEL, HEAD.y,
                S_WIDTH, S_HEIGHT
            )

        if eaten_status:
            APPLE = genet_apple(HEAD, BODY)
            eaten_status = False

        # Draw window
        running = draw_window(HEAD, BODY, APPLE, snake_score)

        pygame.display.update()

    main()


if __name__ == "__main__":
    main()
