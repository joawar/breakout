from vector import *
class Platform():
    def __init__(self, pos, width, height, color):
        self.pos = pos
        self.width = width
        self.height = height
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.pos.x, self.pos.y, self.width, self.height))

    def move(self):
        self.pos.x, filler = pygame.mouse.get_pos()
        self.pos.x -= self.width/2
