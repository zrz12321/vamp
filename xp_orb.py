import pygame
import math

class XPOrb(pygame.sprite.Sprite):
    def __init__(self, x, y, amount=1):
        super(XPOrb, self).__init__()
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.amount = amount  # 这颗球能提供多少 XP

    def update(self, player):
        if not player.is_alive():
            return
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        dist = math.hypot(dx, dy)
        if dist < 80:
            speed = 8
            if dist > 0:
                self.rect.x += (dx / dist) * speed
                self.rect.y += (dy / dist) * speed
            if dist < 20:
                player.gain_xp(self.amount)
                self.kill()

    def draw(self, surface, offset_x, offset_y):
        cx = int(self.rect.centerx - offset_x)
        cy = int(self.rect.centery - offset_y)
        pygame.draw.circle(surface, (50, 255, 100), (cx, cy), 5)
