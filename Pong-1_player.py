# Implementation of classic arcade game Pong, 1-player.
# The code works by going to www.codeskulptor.org and
# pasting it on the left field followed by pressing the 
# 'Play' button located on the top-left corner.
# Use 'w' and 's' to play.

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH/2, HEIGHT/2]
ball_vel = [2, 2]

PAD1_pos = [PAD_WIDTH/2, HEIGHT/2]
PAD2_pos = [WIDTH - PAD_WIDTH/2, HEIGHT/2] 
paddle1_vel = [0, 0]
paddle2_vel = [0, 0]

score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    if direction == RIGHT:
        ball_pos = [WIDTH/2, HEIGHT/2]
        ball_vel = [random.randrange(120, 240)/60, random.randrange(60, 180)/-60]
    elif direction == LEFT:
        ball_pos = [WIDTH/2, HEIGHT/2]
        ball_vel = [random.randrange(120, 240)/-60, random.randrange(60, 180)/-60]   
     

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = score2 = 0
    spawn_ball(RIGHT)

def restart():
    new_game()
            
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]        
    
    # draw scores before the ball...
    canvas.draw_text(str(score1),(140, 100), 60, "Maroon")
    canvas.draw_text(str(score2),(430, 100), 60, "Maroon")
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")
    
    # Collision with upper/lower walls
    if ball_pos[1] <= 0 + BALL_RADIUS or ball_pos[1] >= 400 - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]
    
    # Collision with gutters
    if ball_pos[0] - (BALL_RADIUS - 10) <= PAD_WIDTH:
        sound.play()
        score2 += 1
        spawn_ball(RIGHT)
    if ball_pos[0] + (BALL_RADIUS - 10) >= WIDTH - PAD_WIDTH:
        sound.play()
        score1 += 1
        spawn_ball(LEFT)
    
    # update paddle's vertical position, keep paddle on the screen
    # test whether the current update for a paddle's position will move part of the paddle off 
    # of the screen. If it does, don't allow the update.
    
    PAD1_pos[1] -= paddle1_vel[1]
    if PAD1_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        PAD1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        paddle1_vel[1] = 0
    elif PAD1_pos[1] <= HALF_PAD_HEIGHT:
        PAD1_pos[1] = HALF_PAD_HEIGHT
        paddle1_vel[1] = 0
        
    # Two-player mode    
    """PAD2_pos[1] += paddle2_vel[1]
    if PAD2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        PAD2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        paddle2_vel[1] = 0
    elif PAD2_pos[1] <= HALF_PAD_HEIGHT:
        PAD2_pos[1] = HALF_PAD_HEIGHT
        paddle2_vel[1] = 0"""
    
    # One-player mode
    global paddle2_vel
    PAD2_pos[1] += paddle2_vel[1]
    PAD2_pos[1] = ball_pos[1]
    if paddle2_vel[1] >= 3:
        paddle2_vel = 2
    
    
    # draw paddles
    canvas.draw_line((PAD1_pos[0], PAD1_pos[1] - HALF_PAD_HEIGHT), (PAD1_pos[0], PAD1_pos[1] + HALF_PAD_HEIGHT), PAD_WIDTH, 'Green')
    canvas.draw_line((PAD2_pos[0], PAD2_pos[1] - HALF_PAD_HEIGHT), (PAD2_pos[0], PAD2_pos[1] + HALF_PAD_HEIGHT), PAD_WIDTH, 'Yellow')
    
    # determine whether paddle and ball collide, 
    # horiz. speed increases 10%, but vertical speed increases only 5% to compensate for the paddle speed.
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        if ball_pos[1] > PAD1_pos[1] - (HALF_PAD_HEIGHT + 4) and ball_pos[1] < PAD1_pos[1] + (HALF_PAD_HEIGHT + 4):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.05
            pongsound.play()
    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        if ball_pos[1] > PAD2_pos[1] - (HALF_PAD_HEIGHT + 4) and ball_pos[1] < PAD2_pos[1] + (HALF_PAD_HEIGHT + 4):
            ball_vel[0] = - ball_vel[0] * 1.1
            ball_vel[1] = ball_vel[1] * 1.05
            pongsound.play()
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 6
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = -6
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = -6
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 6
    
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["s"]:
        paddle1_vel[1] = 0
    if key == simplegui.KEY_MAP["up"]:
        paddle2_vel[1] = 0
    if key == simplegui.KEY_MAP["down"]:
        paddle2_vel[1] = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.add_button('Restart', restart, 100) 
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Add sounds
sound = simplegui.load_sound('https://archive.org/download/EvilLaughMale_201506/Evil_Laugh_Male.wav')
pongsound = simplegui.load_sound('https://archive.org/download/pingpong_ball_bounce_201506/pingpong_ball_bounce.wav')
sound.set_volume(0.7)
pongsound.set_volume(0.7)

# start frame
new_game()
frame.start()
