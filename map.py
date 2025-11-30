import pygame
import random
from utils import WORLD_WIDTH, WORLD_HEIGHT


class Decoration:
    """
    Simple world decoration object (tree, rock, bush, etc.)
    Stored in WORLD coordinates, drawn with camera offset.
    """
    def __init__(self, x, y, dtype):
        self.x = x
        self.y = y
        self.dtype = dtype

        if dtype == "tree":
            self.color = (20, 120, 20)
            self.radius = 20
            self.has_trunk = True
        elif dtype == "rock":
            self.color = (130, 130, 130)
            self.radius = 12
            self.has_trunk = False
        elif dtype == "bush":
            self.color = (40, 160, 60)
            self.radius = 15
            self.has_trunk = False
        elif dtype == "bone":  # for graveyard theme
            self.color = (220, 220, 220)
            self.radius = 10
            self.has_trunk = False
        else:
            self.color = (255, 255, 255)
            self.radius = 10
            self.has_trunk = False

    def draw(self, surface, offset_x, offset_y):
        sx = int(self.x - offset_x)
        sy = int(self.y - offset_y)

        # Only draw if visible on screen (small cull)
        if sx < -50 or sx > surface.get_width() + 50:
            return
        if sy < -50 or sy > surface.get_height() + 50:
            return

        pygame.draw.circle(surface, self.color, (sx, sy), self.radius)

        # simple tree trunk
        if self.has_trunk:
            pygame.draw.rect(
                surface,
                (90, 60, 40),
                (sx - 4, sy + self.radius - 6, 8, 10)
            )


class Map:
    """
    A map instance: holds theme, tile colors, and decorations.

    Example types:
      - "forest"
      - "desert"
      - "graveyard"
    You can add more later easily.
    """
    def __init__(self, map_type="forest", seed=None):
        self.map_type = map_type
        self.tile_size = 80
        self.rng = random.Random(seed)
        self.decorations = []

        # Theme setup (tile colors + decoration settings)
        self._setup_theme()
        # Generate random decorations over the whole world
        self._generate_decorations()

    # ---------------- THEME SETUP ----------------
    def _setup_theme(self):
        if self.map_type == "forest":
            # ground colors
            self.base_color = (30, 80, 30)
            self.alt_color = (25, 70, 25)
            self.decoration_types = ["tree", "tree", "bush", "rock"]
            self.decoration_count = 140

        elif self.map_type == "desert":
            self.base_color = (180, 160, 80)
            self.alt_color = (190, 170, 90)
            self.decoration_types = ["rock", "rock", "bush"]
            self.decoration_count = 90

        elif self.map_type == "graveyard":
            self.base_color = (40, 40, 60)
            self.alt_color = (35, 35, 55)
            self.decoration_types = ["rock", "bone", "bush"]
            self.decoration_count = 110

        else:
            # default / unknown map type
            self.base_color = (40, 80, 40)
            self.alt_color = (35, 75, 35)
            self.decoration_types = ["tree", "bush", "rock"]
            self.decoration_count = 100

    # ------------- DECORATION GENERATION -------------
    def _generate_decorations(self):
        self.decorations.clear()

        for _ in range(self.decoration_count):
            x = self.rng.randint(60, WORLD_WIDTH - 60)
            y = self.rng.randint(60, WORLD_HEIGHT - 60)
            dtype = self.rng.choice(self.decoration_types)
            self.decorations.append(Decoration(x, y, dtype))

    # ------------- DRAW BACKGROUND TILES -------------
    def draw_background(self, surface, offset_x, offset_y):
        """
        Draws large colored tiles for the ground.
        Uses WORLD coordinates and camera offset.
        """
        tile = self.tile_size
        width = surface.get_width()
        height = surface.get_height()

        # Figure out which tiles are visible
        start_x = int(offset_x // tile) * tile
        start_y = int(offset_y // tile) * tile

        for gx in range(start_x, start_x + width + tile, tile):
            for gy in range(start_y, start_y + height + tile, tile):
                # Screen-space position
                sx = gx - offset_x
                sy = gy - offset_y

                # checkerboard / variation
                ix = gx // tile
                iy = gy // tile
                if (ix + iy) % 2 == 0:
                    color = self.base_color
                else:
                    color = self.alt_color

                pygame.draw.rect(surface, color, (sx, sy, tile, tile))

    # ------------- DRAW DECORATIONS -------------
    def draw_decorations(self, surface, offset_x, offset_y):
        for deco in self.decorations:
            deco.draw(surface, offset_x, offset_y)
