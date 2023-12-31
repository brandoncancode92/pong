# Imports
import pygame
# Initialize pygame
pygame.init()

# Set game window
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong") # Setting the game title on the display window

FPS = 60 # Frames per second
# Color values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 50)
WINNING_SCORE = 5

# Classes

# Paddle class
class Paddle:
    # Class attributes apply to all instances of the class
    COLOR = WHITE
    VEL = 4

    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y , self.width, self.height))

    # Move the paddle up and down
    def move(self, up=True):
        if up:
            self.y -= self.VEL
        else:
            self.y += self.VEL

    # Reset the paddles
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# Ball class
class Ball:
    # Class attributes
    MAX_VEL = 5
    COLOR = WHITE

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    # Draw the pong ball
    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Resetting the ball
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

# Draw function
def draw(win, paddles, ball, left_score, right_score): # win stands for (game window)
    win.fill(BLACK) # Window color

    # Drawing the scores
    left_score_text = SCORE_FONT.render(f'{left_score}', 1, WHITE)
    right_score_text = SCORE_FONT.render(f'{right_score}', 1, WHITE)
    win.blit(left_score_text, (WIDTH // 4 - left_score_text.get_width() // 2, 20))
    win.blit(right_score_text, (WIDTH *  (3/ 4) - right_score_text.get_width() // 2, 20))

    # Draw both paddles
    for paddle in paddles:
        paddle.draw(win)

    # Draw line down the center of the window
    for i in range(10, HEIGHT, HEIGHT // 20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win, WHITE, (WIDTH // 2 - 5, i, 10, HEIGHT // 20))

    ball.draw(win)
    pygame.display.update() # Update the game window (This should only be done after all the drawing is done)


# Ball collision logic
def handle_collision(ball, left_paddle, right_paddle):
    # Ceiling/floor logic
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Collision with left paddle
    # X axis
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # Y axis
                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel

    # Collision with right paddle
    # X axis
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                # Y axis
                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


# Paddle Movement
def handle_paddle_movement(keys, left_paddle, right_paddle):
    # Left Paddle
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VEL >= 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VEL + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    # Right Paddle
    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VEL >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VEL + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)


# Event function that displays the game window and draws something on it
def main():
    run = True
    clock = pygame.time.Clock() # Regulate the frame rate of our game
    left_score = 0
    right_score = 0

    # Paddle instances
    left_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH - 10 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Ball instance
    ball = Ball(WIDTH // 2, HEIGHT // 2, BALL_RADIUS)


    # Main event loop
    while run:
        clock.tick(FPS)
        draw(WIN, [left_paddle, right_paddle], ball, left_score, right_score) # Window that we want to draw on

        for event in pygame.event.get():
            if event .type == pygame.QUIT:
                run = False
                break


        keys = pygame.key.get_pressed()
        handle_paddle_movement(keys, left_paddle, right_paddle)

        ball.move()
        handle_collision(ball, left_paddle, right_paddle)

        # Score
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # Winning the game
        won = False

        if left_score >= WINNING_SCORE:
            won = True
            win_text = "Left Player Won!"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "Right Player Won!"

        if won:
            text = SCORE_FONT.render(win_text, 1, WHITE)
            WIN.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(4000)
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

# Ensure that we are running this module to call the main function
if __name__ == '__main__':
    main()