import pygame
import random

# --------------------------------------------
# SCREEN & WORLD SETTINGS
# --------------------------------------------
WIDTH = 1280
HEIGHT = 720

WORLD_WIDTH = 3000
WORLD_HEIGHT = 2000

screen = pygame.display.set_mode((WIDTH, HEIGHT))


# --------------------------------------------
# CAMERA
# --------------------------------------------
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self, target_x, target_y):
        # Center camera on target
        self.x = target_x - WIDTH // 2
        self.y = target_y - HEIGHT // 2

        # Clamp to world bounds
        self.x = max(0, min(self.x, WORLD_WIDTH - WIDTH))
        self.y = max(0, min(self.y, WORLD_HEIGHT - HEIGHT))


# --------------------------------------------
# SPAWN ENEMIES OUTSIDE CAMERA VIEW
# --------------------------------------------

SPAWN_MARGIN = 180  # distance OUTSIDE the screen enemies appear

def get_spawn_position(camera):
    """Spawn enemies OUTSIDE the player's camera view (true off-screen)."""

    left = camera.x
    right = camera.x + WIDTH
    top = camera.y
    bottom = camera.y + HEIGHT

    side = random.randint(0, 3)

    if side == 0:  # left
        x = left - SPAWN_MARGIN
        y = random.randint(top - SPAWN_MARGIN, bottom + SPAWN_MARGIN)

    elif side == 1:  # right
        x = right + SPAWN_MARGIN
        y = random.randint(top - SPAWN_MARGIN, bottom + SPAWN_MARGIN)

    elif side == 2:  # top
        x = random.randint(left - SPAWN_MARGIN, right + SPAWN_MARGIN)
        y = top - SPAWN_MARGIN

    else:  # bottom
        x = random.randint(left - SPAWN_MARGIN, right + SPAWN_MARGIN)
        y = bottom + SPAWN_MARGIN

    return x, y


# --------------------------------------------
# COLORS
# --------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 30, 30)
GREEN = (30, 200, 30)
YELLOW = (255, 220, 50)
BLUE = (50, 120, 255)
