from vector import *
from platform import Platform
from ball import Ball
from brick import Brick
from config import *
import numpy as np


pygame.init()
screen = pygame.display.set_mode(SCREEN_RES)
clock = pygame.time.Clock()
started = False
screen_height = screen.get_height()
screen_width = screen.get_width()  

def make_bricks():
    """Makes the bricks and places them on the screen, and returns a list containing all of them
    """
    brick_x_arr = np.linspace(LEFTMOST_BRICK_X, RIGHTMOST_BRICK_X, BRICKS_PER_ROW)
    brick_y_arr = np.linspace(BOTTOM_ROW_Y, TOP_ROW_Y, NUMBER_OF_ROWS)
    brick_arr = []
    for x in brick_x_arr:
        for y in brick_y_arr:
            pos = Vector2(x,y)
            brick = Brick(pos, BRICK_WIDTH, BRICK_HEIGHT, BRICK_COLOR) 
            brick_arr.append(brick)
    return brick_arr

# make platform
platform = Platform(PLATFORM_POS, PLATFORM_WIDTH, PLATFORM_HEIGHT, PLATFORM_COLOR)

# make ball
ball = Ball(BALL_POS, BALL_RADIUS, BALL_COLOR)

# make bricks
brick_arr = make_bricks()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    # make a black background     
    pygame.draw.rect(screen, (0,0,0), (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # limit to 30FPS
    time_passed = clock.tick(FPS)  
    time_passed_seconds = time_passed / 1000.0

    # move platform
    platform.move()
    platform.draw(screen)

    # move ball
    ball.move()
    ball.draw(screen)

    # draw bricks
    for brick in brick_arr:
        brick.draw(screen)
    
    # at mouse click, set start velocity
    if not started:
        ball.pos.x = platform.pos.x + platform.width/2
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left mouse click
                    started = True
                    ball.start()
    # check if the ball has collided with anything
    # right wall
    if ball.pos.x > SCREEN_WIDTH - ball.radius:
        ball.velocity.x = -abs(ball.velocity.x) 
    
    # left wall
    if ball.pos.x < ball.radius:
        ball.velocity.x = abs(ball.velocity.x)

    # roof
    if ball.pos.y <= 0:
        ball.velocity.y = abs(ball.velocity.y)

    # floor
    if ball.pos.y >= SCREEN_HEIGHT:
        print("You lost")
        break

    # blocks
    for brick in brick_arr:
        impulse = intersect_rectangle_circle(brick.pos, brick.width, brick.height, ball.pos, ball.radius, ball.velocity)
        if impulse:
            brick_arr.remove(brick)
            ball.set_new_velocity(impulse)
    
    # platform
    try:
        impulse = intersect_rectangle_circle(platform.pos, platform.width, platform.height, ball.pos, ball.radius, ball.velocity)
    except ValueError:
        impulse = False
    if impulse:
        platform_circle_x = platform.pos.x + platform.width/2
        platform_circle_y = platform.pos.y + platform.height/2
        platform_circle_radius = platform.width
        platform_circle_pos = Vector2(platform_circle_x, platform_circle_y)
        impulse2 = intersect_circles(platform_circle_pos, platform_circle_radius, ball.pos, ball.radius)
        ball.set_new_velocity(impulse2)

    # if the blocks are all gone the player wins
    if len(brick_arr) == 0:
        print("You won")
        break
    
    pygame.display.update()