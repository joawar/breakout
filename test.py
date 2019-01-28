from pygame.math import Vector2
import pygame

test = Vector2(1,1)
test = test * test.length()
print(test.length())