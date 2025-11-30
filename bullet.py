import pygame
import math
from utils import WORLD_WIDTH, WORLD_HEIGHT  # Added world dimensions

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x + math.cos(angle) * 45
        self.y = y + math.sin(angle) * 45
        self.angle = angle
        self.speed = 18
        self.radius = 7

    def update(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed

    def draw(self, surface, offset_x, offset_y):  # Added offset parameters
        # Draw with camera offset
        draw_x = int(self.x - offset_x)
        draw_y = int(self.y - offset_y)
        pygame.draw.circle(surface, (255, 220, 0), (draw_x, draw_y), self.radius)

    def off_screen(self):
        # Check against world boundaries instead of screen
        return not (-50 <= self.x <= WORLD_WIDTH + 50 and -50 <= self.y <= WORLD_HEIGHT + 50)