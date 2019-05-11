import play # this should always be the first line
import cv2
from tracking_camera import show_webcam, setup_mouth_tracker

p1_box = play.new_box(color='blue', transparency=50, x=350, y=0, width=30, height=120)
p2_box = play.new_box(color='green', transparency=50, x=350, y=0, width=30, height=120)
overlap_box = play.new_box(color='purple', transparency=100, border_width=3, border_color='red', x=350, y=0, width=30, height=120)
debug_print = play.new_text('coordinates', font_size=20)

ai_box = play.new_box(color='black', x=-350, y=0, width=30, height=120)
ai_box.dy = 3

ball = play.new_box(color='dark red', x=0, y=0, width=20, height=20)
ball.dx = 2
ball.dy = -1

cam, mouth_cascade = setup_mouth_tracker()

# start up the webcam window
frame = show_webcam(cam)
cv2.imshow('Mouth Detector', frame)

@play.repeat_forever
async def do():
    frame = show_webcam(cam)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    mouth_rects = mouth_cascade.detectMultiScale(gray, 1.7, 11)

    if len(mouth_rects) > 0:
        # convert cam input to screen coordinates
        cam_height = frame.shape[1]
        screen_height = play.screen.height
        raw_y_coordinate = mouth_rects[0][1]
        ypos = (raw_y_coordinate / cam_height)
        y_coordinate = (-1 * ypos) * screen_height
        p1_box.y = y_coordinate
        # if len(mouth_rects) > 1:
        #     p2_box.y = mouth_rects[1][1]

        debug_print.words = f'raw_y: {raw_y_coordinate}, ypos: {ypos}, y_coordinate: {y_coordinate}'

        for (x,y,w,h) in mouth_rects:
            y = int(y - 0.15*h)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)
            break

    cv2.imshow('Mouth Detector', frame)
        
# make the ball move
@play.repeat_forever
async def do():
    ball.x += ball.dx
    ball.y += ball.dy

# make the ball bounce off the player's paddle
@play.repeat_forever
async def do():
    if (ball.right >= overlap_box.left) and (ball.top >= overlap_box.bottom) and (ball.bottom <= overlap_box.top) and (ball.left < overlap_box.left):
        ball.dx = -2

@play.repeat_forever
async def do():
    # find the overlap of the two player paddles
    overlap_top = min(p1_box.top, p2_box.top)
    overlap_bottom = max(p1_box.bottom, p2_box.bottom)

    # set the position and height of the "combined paddle"
    # that represents the overlap of the two players paddles

    if overlap_top > overlap_bottom:
        overlap_box.y = (overlap_top + overlap_bottom) / 2
        overlap_box.height = (overlap_top - overlap_bottom)
    else:
        overlap_box.height = 0

    # debug_print.words = f'p1_box: [{p1_box.top},{p1_box.bottom}], p2_box: [{p2_box.top},{p2_box.bottom}], overlap: [{overlap_box.top},{overlap_box.bottom}]'


# make the computer player follow the ball
@play.repeat_forever
async def do():
    if ball.x < 0 and abs(ball.y-ai_box.y) > ai_box.dy:
        if ai_box.y < ball.y:
            ai_box.y += ai_box.dy
        elif ai_box.y > ball.y:
            ai_box.y -= ai_box.dy

# make the ball bounce off the computer player's paddle
@play.repeat_forever
async def do():
    if (ball.left <= ai_box.right) and (ball.top >= ai_box.bottom) and (ball.bottom <= ai_box.top) and (ball.right > ai_box.right):
        ai_box.dy = play.random_number(1, 4)
        ball.dx = 2

@play.repeat_forever
async def do():
    keys_pressed = []
    if play.key_is_pressed('o'):
        p1_box.y += 10
    if play.key_is_pressed('k'):
        p1_box.y -= 10
    if play.key_is_pressed('w'):
        p2_box.y += 10
    if play.key_is_pressed('s'):
        p2_box.y -= 10

# make ball bounce off bottom and top walls
@play.repeat_forever
async def do():
    if ball.bottom <= play.screen.bottom:
        ball.dy = 1
    elif ball.top >= play.screen.top:
        ball.dy = -1

play.start_program() # this should always be the last line