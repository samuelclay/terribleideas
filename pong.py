import play # this should always be the first line
import cv2
from tracking_camera import find_mouth_rects

p1_box = play.new_box(color='blue', transparency=50, x=350, y=0, width=30, height=120)
p2_box = play.new_box(color='green', transparency=50, x=350, y=0, width=30, height=120)
overlap_box = play.new_box(color='purple', transparency=100, border_width=3, border_color='red', x=350, y=0, width=30, height=120)
debug_print = play.new_text('coordinates', font_size=20)

ai_box = play.new_box(color='black', x=-350, y=0, width=30, height=120)
ai_box.dy = 3

ball = play.new_box(color='dark red', x=0, y=0, width=20, height=20)
ball.dx = 4
ball.dy = -1

@play.repeat_forever
async def do():
    left_img, left_mouth_rects, right_mouth_rects = find_mouth_rects()
    
    def y_coord_from_mouth_rect(mouth_rects, box):
        if len(mouth_rects) > 0:
            # convert cam input to screen coordinates
            debug_print.words = f'mouth_rects: {left_img.shape}, mouth_rects: {mouth_rects[0][1]}'
            
            cam_height = left_img.shape[1]
            screen_height = play.screen.height
            raw_y_coordinate = mouth_rects[0][1] / 2

            # ypos represents mouth position as a percentage.
            # in the opencv code we halve the image size;
            # account for that here by dividing cam height by 2
            ypos = (raw_y_coordinate / cam_height)

            # convert the percentage y position to an absolute
            # coordinate in the play coordinate system
            # (0 is middle, 0.5 * screen height is top of screen)
            y_coordinate = (0.5 - ypos) * screen_height
            box.y = y_coordinate
            # debug_print.words = f'cam_height: {cam_height}, raw_y: {raw_y_coordinate}, ypos: {ypos}, y_coordinate: {y_coordinate}'
    
    y_coord_from_mouth_rect(left_mouth_rects, p1_box)
    y_coord_from_mouth_rect(right_mouth_rects, p2_box)
        
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

# make ball come back from left and right
@play.repeat_forever
async def do():
    if ball.x <= play.screen.left:
        ball.x = play.screen.right
    elif ball.x >= play.screen.right:
        ball.x = play.screen.left


play.start_program() # this should always be the last line