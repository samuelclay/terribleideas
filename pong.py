import play # this should always be the first line
import cv2
from tracking_camera import find_mouth_rects

# p1_box = play.new_box(color='blue', x=350, y=0, width=30, height=120)
# p2_box = play.new_box(color='red', x=-350, y=0, width=30, height=120)

background = play.new_image(image='background.jpg', x=0, y=0, size=200, transparency=30)

play.new_text("MOUTH PONG", x=0, y=250)

p1_box = play.new_image(image='mouth-vertical.png', x=350, y=0, size=200)
p2_box = play.new_image(image='mouth-vertical.png', x=-350, y=0, size=200)

ball = play.new_image(image='heart.png', x=0, y=0, size=30)
ball.dx = 10
ball.dy = -1

trailing_ball_1 = play.new_image(image='heart.png', x=0, y=0, size=30, transparency=30)
trailing_ball_2 = play.new_image(image='heart.png', x=0, y=0, size=30, transparency=10)

frame_count = 0
debug_print = play.new_text('coordinates', font_size=20)

@play.repeat_forever
async def do():
    global frame_count
    frame_count += 1
    if frame_count % 5 != 1:
        return

    # update the background
    # global background
    # old_background = background
    # background = play.new_image(image='background.jpg', x=0, y=0, size=200, transparency=50)
    # old_background.remove()
    
    left_img, left_mouth_rects, right_mouth_rects, left_smile, right_smile = find_mouth_rects()
    
    def y_coord_from_mouth_rect(mouth_rects, box):
        if len(mouth_rects) > 0:            
            
            cam_height = left_img.shape[1]
            cam_width = left_img.shape[0]
            screen_height = play.screen.height
            screen_width = play.screen.width
            
            raw_x_coordinate = mouth_rects[0][0]
            raw_y_coordinate = mouth_rects[0][1] * 2
            
            xpos = (raw_x_coordinate / cam_width)
            negative = -1 if box.x < 0 else 1
            if not negative:
                xpos = 200 - xpos
            x_coordinate = negative * 350 + (xpos*50)
            box.x = x_coordinate

            # ypos represents mouth position as a percentage.
            # in the opencv code we halve the image size;
            # account for that here by dividing cam height by 2
            ypos = (raw_y_coordinate / cam_height)
            
            if len(left_smile) == 0 and negative:
                ypos = 1 - ypos
            elif len(right_smile) == 0 and not negative:
                ypos = 1 - ypos
                
            # convert the percentage y position to an absolute
            # coordinate in the play coordinate system
            # (0 is middle, 0.5 * screen height is top of screen)
            y_coordinate = (0.5 - ypos) * screen_height
            box.y = y_coordinate

            global p1_box
            global p2_box

            if len(right_mouth_rects) > 0:
                old_p1_box = p1_box
                p1_box = play.new_image(image='right_mouth.jpg', x=old_p1_box.x, y=old_p1_box.y, size=200)
                old_p1_box.remove()
            if len(left_mouth_rects) > 0:
                old_p2_box = p2_box
                p2_box = play.new_image(image='left_mouth.jpg', x=old_p2_box.x, y=old_p2_box.y, size=200)
                old_p2_box.remove()
    
    y_coord_from_mouth_rect(right_mouth_rects, p1_box)
    y_coord_from_mouth_rect(left_mouth_rects, p2_box)

        
# make the ball move
@play.repeat_forever
async def do():
    global frame_count
    if frame_count % 5 == 1:
        global trailing_ball_1
        global trailing_ball_2

        trailing_ball_2.x = trailing_ball_1.x
        trailing_ball_2.y = trailing_ball_1.y

        trailing_ball_1.x = ball.x
        trailing_ball_1.y = ball.y

    ball.x += ball.dx
    ball.y += ball.dy

# make the ball bounce off the player's paddle
@play.repeat_forever
async def do():
    if (ball.right >= p1_box.left) and (ball.top >= p1_box.bottom) and (ball.bottom <= p1_box.top) and (ball.left < p1_box.left):
        ball.dx = -1 * ball.dx
    if (ball.left <= p2_box.right) and (ball.top >= p2_box.bottom) and (ball.bottom <= p2_box.top) and (ball.right > p2_box.right):
        ball.dx = -1 * ball.dx

# @play.repeat_forever
# async def do():
#     keys_pressed = []
#     if play.key_is_pressed('o') and p1_box.top < play.screen.top:
#         p1_box.y += 10
#     if play.key_is_pressed('k') and p1_box.bottom > play.screen.bottom:
#         p1_box.y -= 10
#     if play.key_is_pressed('w') and p2_box.top < play.screen.top:
#         p2_box.y += 10
#     if play.key_is_pressed('s') and p2_box.bottom > play.screen.bottom:
#         p2_box.y -= 10

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