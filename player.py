import pygame
from utils import WORLD_WIDTH, WORLD_HEIGHT


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, hp=100, speed=4, color=(100, 200, 255)):
        super().__init__()

        # -------------------------
        # Core Stats
        # -------------------------
        self.max_health = hp
        self.health = hp
        self.speed = speed
        self.color = color

        # Set by character selection
        self.base_damage = 10
        self.base_range = 120

        # -------------------------
        # XP & Leveling System
        # -------------------------
        self.level = 1

        # XP inside the current level
        self.xp = 0

        # XP needed for next level
        self.xp_required = 10

        # Shows upgrade window
        self.pending_upgrade = False

        # Total XP gained (used for XP bar text)
        self.xp_total = 0

        # -------------------------
        # Sprite
        # -------------------------
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (15, 15), 15)
        self.rect = self.image.get_rect(center=(x, y))

    # -------------------------------------------------
    # MOVEMENT
    # -------------------------------------------------
    def update(self):
        if not self.is_alive():
            return

        keys = pygame.key.get_pressed()
        dx = (keys[pygame.K_d] - keys[pygame.K_a]) * self.speed
        dy = (keys[pygame.K_s] - keys[pygame.K_w]) * self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Stay inside world bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WORLD_HEIGHT))

    # -------------------------------------------------
    # XP SYSTEM
    # -------------------------------------------------
    def gain_xp(self, amount):
        """Enemies call this to reward XP."""
        if not self.is_alive():
            return

        self.xp += amount
        self.xp_total += amount

        # Only trigger a pending upgrade once
        if self.xp >= self.xp_required and not self.pending_upgrade:
            self.pending_upgrade = True

    def has_level_up_ready(self):
        return self.pending_upgrade

    def finish_level_up(self):
        """Called when player selects a stat upgrade."""
        # Preserve leftover XP (fixes the 24/10 → 14/22 bug)
        leftover = self.xp - self.xp_required
        if leftover < 0:
            leftover = 0

        # Level up
        self.level += 1
        self.pending_upgrade = False

        # Increase XP requirement
        self.xp_required = int(self.xp_required * 1.45)

        # Apply leftover XP toward new level
        self.xp = leftover

        # 🟦 Auto-trigger another upgrade if leftover XP is already enough
        if self.xp >= self.xp_required:
            self.pending_upgrade = True

    # -------------------------------------------------
    # HEALTH
    # -------------------------------------------------
    def is_alive(self):
        return self.health > 0

    # -------------------------------------------------
    # DRAW PLAYER + HEALTH BAR + XP BAR
    # -------------------------------------------------
    def draw(self, surface, ox, oy):
        # World → screen position
        cx = int(self.rect.centerx - ox)
        cy = int(self.rect.centery - oy)

        # Player body
        pygame.draw.circle(surface, self.color, (cx, cy), 15)

        # HEALTH BAR
        bar_w = 40
        hp_fill = max(0, (self.health / self.max_health) * bar_w)
        pygame.draw.rect(surface, (150, 0, 0), (cx - 20, cy - 30, bar_w, 6))
        pygame.draw.rect(surface, (0, 200, 0), (cx - 20, cy - 30, hp_fill, 6))

        # -------------------------------
        # XP BAR (FULL WIDTH BOTTOM)
        # -------------------------------
        xp_ratio = min(self.xp / self.xp_required, 1.0)
        screen_w = surface.get_width()
        screen_h = surface.get_height()

        pygame.draw.rect(surface, (40, 40, 40), (0, screen_h - 25, screen_w, 25))
        pygame.draw.rect(surface, (80, 150, 255),
                         (0, screen_h - 25, screen_w * xp_ratio, 25))

        # XP TEXT
        font = pygame.font.Font(None, 28)
        txt = font.render(
            f"XP: {self.xp_total} (Lvl {self.level})  [{self.xp}/{self.xp_required}]",
            True, (255, 255, 255)
        )
        surface.blit(txt, (10, screen_h - 23))

    # -------------------------------------------------
    # MINIMAP DOT
    # -------------------------------------------------
    def draw_minimap(self, surface, rect):
        mini_x = int((self.rect.centerx / WORLD_WIDTH) * rect.width)
        mini_y = int((self.rect.centery / WORLD_HEIGHT) * rect.height)

        pygame.draw.circle(surface, (0, 255, 0),
                           (rect.x + mini_x, rect.y + mini_y), 3)
