"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman, 
and Jerry Liao.

YOUR DESCRIPTION HERE
Name: Ester
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing
BRICK_WIDTH = 40       # Height of a brick (in pixels)
BRICK_HEIGHT = 15      # Height of a brick (in pixels)
BRICK_ROWS = 10        # Number of rows of bricks
BRICK_COLS = 10        # Number of columns of bricks
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels)
BALL_RADIUS = 10       # Radius of the ball (in pixels)
PADDLE_WIDTH = 75      # Width of the paddle (in pixels)
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels)
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels)
INITIAL_Y_SPEED = 7    # Initial vertical speed for the ball
MAX_X_SPEED = 5        # Maximum initial horizontal speed for the ball


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH, paddle_height=PADDLE_HEIGHT,
                 paddle_offset=PADDLE_OFFSET, brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS, brick_width=BRICK_WIDTH,
                 brick_height=BRICK_HEIGHT, brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING, title='Breakout'):

        # Create a graphical window, with some extra space
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Create a paddle
        self.paddle = GRect(paddle_width, paddle_height)
        self.paddle.filled = True
        self.window.add(self.paddle, x=(self.window.width - self.paddle.width)/2,
                        y=self.window.height - paddle_offset - self.paddle.height)

        # Center a filled ball in the graphical window
        self.ball = GOval(ball_radius*2, ball_radius*2)
        self.ball.filled = True
        self.reset_ball()

        # Default initial velocity for the ball
        self.__dy = 0
        self.__dx = 0

        # Initialize our mouse listeners
        self.__start = False
        self.__break_brick = False
        onmouseclicked(self.start_game)
        onmousemoved(self.set_paddle_position)

        # Draw bricks
        brick_y = BRICK_OFFSET
        for i in range(brick_rows):
            brick_x = 0
            for j in range(brick_cols):
                self.brick = GRect(brick_width, brick_height)
                self.window.add(self.brick, x=brick_x, y=brick_y)
                brick_x += brick_width + brick_spacing
                self.brick.filled = True
                if i % 2 == 0:
                    self.brick.fill_color = 'lightslategray'
                else:
                    self.brick.fill_color = 'lightsteelblue'
            brick_y += self.brick.height + brick_spacing

        # count brick qty
        self.__brick_qty = brick_rows * brick_cols

    def get_brick_qty(self):
        # get total amounts of brick
        return self.__brick_qty

    def start_game(self, mouse):
        # control ball's moving action
        self.__start = True

    def get_start(self):
        # get ball's moving active
        return self.__start

    def set_paddle_position(self, mouse):
        # set paddle position
        if self.paddle.width / 2 <= mouse.x <= self.window.width - self.paddle.width / 2:
            self.paddle.x = mouse.x - self.paddle.width / 2

    def reset_ball(self):
        # the ball default setting
        self.set_ball_velocity()
        self.window.add(self.ball, x=(self.window.width - self.ball.width) / 2, y=(self.window.height - self.ball.height) / 2)
        self.__start = False

    def set_ball_velocity(self):
        # set_ball_velocity
        self.__dy = INITIAL_Y_SPEED
        self.__dx = random.randint(1, MAX_X_SPEED)
        if random.random() > 0.5:
            self.__dx = -self.__dx

    def get_vx(self):
        # get horizontal speed for the ball
        return self.__dx

    def get_vy(self):
        # get vertical speed for the ball
        return self.__dy

    def check_collision(self):
        # check the collision, paddle or brick
        for x in range(int(self.ball.x), int(self.ball.x)+self.ball.width+1, self.ball.width):
            for y in range(int(self.ball.y), int(self.ball.y)+self.ball.height+1, self.ball.height):
                obj = self.window.get_object_at(x, y)
                if obj is not None:
                    if obj != self.paddle:
                        self.window.remove(obj)
                        self.__break_brick = True
                    else:
                        self.__break_brick = False
                    return self.__break_brick
