from vector import *
from config import *
class Ball():
    def __init__(self, pos, radius, color):
        """Initializes the ball object
        
        Arguments:
            pos {Vector2} -- the position of the ball
            radius {float} -- the radius of the ball
            color {tuple} -- the color of the ball given as RGB tuple, e.g. (255,0,0) is red
        """
        self.pos = pos
        self.radius = round(radius)
        self.velocity = Vector2(0,0)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (round(self.pos.x), round(self.pos.y)), self.radius)

    def move(self):
        self.pos += self.velocity

    def start(self):
        self.velocity = BALL_START_VELOCITY
    
    def set_new_velocity(self, velocity):
        new_velocity = velocity * self.velocity.length()
        self.velocity = new_velocity 