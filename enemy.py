import pygame
import math


class Enemy(pygame.sprite.Sprite):
    """Base class for all enemies."""
    def __init__(self, x, y, hp, speed, color, xp_reward):
        super().__init__()

        # --- Core stats ---
        self.health = hp
        self.max_health = hp        # ✔ FIXED: needed for correct HP bar
        self.speed = speed
        self.color = color
        self.xp_reward = xp_reward

        # Sprite
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (10, 10), 10)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player):
        """Move toward player."""
        if not player.is_alive():
            return

        px, py = player.rect.center
        ex, ey = self.rect.center

        dx = px - ex
        dy = py - ey
        dist = math.hypot(dx, dy)

        if dist != 0:
            self.rect.x += (dx / dist) * self.speed
            self.rect.y += (dy / dist) * self.speed

        # Enemy touches player
        if self.rect.colliderect(player.rect):
            player.health -= 10
            self.health = 0  # dies on contact

    def handle_death(self, xp_group):
        """Add XP orbs and remove enemy."""
        if self.health <= 0:
            from xp_orb import XPOrb
            xp_group.add(XPOrb(self.rect.centerx, self.rect.centery, self.xp_reward))
            self.kill()

    def draw(self, surface, ox, oy):
        cx = self.rect.centerx - ox
        cy = self.rect.centery - oy

        # Enemy circle
        pygame.draw.circle(surface, self.color, (cx, cy), 10)

        # HP bar
        bar_w = 20
        hp_ratio = max(self.health / self.max_health, 0)   # ✔ FIXED

        pygame.draw.rect(surface, (150, 0, 0), (cx - 10, cy - 18, bar_w, 4))
        pygame.draw.rect(surface, (0, 200, 0), (cx - 10, cy - 18, bar_w * hp_ratio, 4))


# ---------------------------------------------------------
# ENEMY TYPES
# ---------------------------------------------------------
class BasicEnemy(Enemy):
    def __init__(self, x, y, scale=1.0):
        hp = int(25 * scale)
        speed = 1.6
        color = (255, 80, 80)
        xp_reward = 3
        super().__init__(x, y, hp, speed, color, xp_reward)


class FastEnemy(Enemy):
    def __init__(self, x, y, scale=1.0):
        hp = int(15 * scale)
        speed = 3.2
        color = (255, 255, 80)
        xp_reward = 2
        super().__init__(x, y, hp, speed, color, xp_reward)


class TankEnemy(Enemy):
    def __init__(self, x, y, scale=1.0):
        hp = int(60 * scale)
        speed = 0.9
        color = (140, 40, 40)
        xp_reward = 5
        super().__init__(x, y, hp, speed, color, xp_reward)
