import pygame
import random
from utils import WIDTH, HEIGHT, screen, get_spawn_position
from enemy import BasicEnemy, FastEnemy, TankEnemy


class GameManager:
    def __init__(self, weapon_manager):
        self.weapon_manager = weapon_manager

        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 40)

        self.time = 0.0
        self.spawn_timer = 0

        self.show_upgrade = False
        self.game_over = False

        # Upgrade buttons
        self.button_rects = [
            pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 - 80, 360, 60),
            pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 - 10, 360, 60),
            pygame.Rect(WIDTH // 2 - 180, HEIGHT // 2 + 60, 360, 60),
        ]

    # ------------------------------------------------------------
    def check_mouse_click(self, pos):
        for i, rect in enumerate(self.button_rects, start=1):
            if rect.collidepoint(pos):
                return i
        return 0

    # ------------------------------------------------------------
    def update(self, player, enemies, xp_orbs, camera):
        if player.health <= 0:
            self.game_over = True
            return

        self.time += 1 / 60
        self.spawn_timer += 1

        # difficulty
        scale = 1.0 + player.level * 0.18 + self.time / 200.0

        # pick type
        if self.time < 60:
            enemy_class = BasicEnemy
        elif self.time < 180:
            enemy_class = random.choices(
                [BasicEnemy, FastEnemy],
                weights=[3, 1],
                k=1
            )[0]
        else:
            enemy_class = random.choices(
                [BasicEnemy, FastEnemy, TankEnemy],
                weights=[3, 2, 2],
                k=1
            )[0]

        # spawn rate
        rate = max(25 - int(self.time // 20), 8)
        if self.spawn_timer >= rate:
            sx, sy = get_spawn_position(camera)
            enemies.add(enemy_class(sx, sy, scale))
            self.spawn_timer = 0

    # ------------------------------------------------------------
    def draw(self, player, mouse_pos):
        # Time
        screen.blit(self.small_font.render(f"Time: {int(self.time)}s", True, (255, 255, 255)), (10, 10))

        # Level
        screen.blit(self.small_font.render(f"LVL {player.level}", True, (255, 255, 120)), (10, 50))

        # Hint
        if player.has_level_up_ready() and not self.show_upgrade and not self.game_over:
            hint = self.small_font.render("Press ESC to choose upgrade", True, (255, 255, 180))
            screen.blit(hint, (WIDTH // 2 - 200, HEIGHT - 80))

        # Level-up menu
        if self.show_upgrade:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(180)
            overlay.fill((0, 0, 0))
            screen.blit(overlay, (0, 0))

            title = self.font.render("LEVEL UP!", True, (255, 255, 120))
            screen.blit(title, (WIDTH // 2 - 160, HEIGHT // 2 - 200))

            options = ["SPEED ++", "DAMAGE ++", "RANGE ++"]

            for text, rect in zip(options, self.button_rects):
                hovered = rect.collidepoint(mouse_pos)
                pygame.draw.rect(screen, (60, 60, 90), rect)
                pygame.draw.rect(screen,
                                 (255, 255, 120) if hovered else (120, 120, 120),
                                 rect, 3)
                t = self.font.render(text, True, (255, 255, 255))
                screen.blit(t, t.get_rect(center=rect.center))

        # Game over
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(220)
            overlay.fill((100, 0, 0))
            screen.blit(overlay, (0, 0))

            title = self.font.render("GAME OVER", True, (255, 80, 80))
            screen.blit(title, (WIDTH // 2 - 200, HEIGHT // 2 - 150))

            restart = self.small_font.render("Press R to Restart", True, (255, 255, 0))
            screen.blit(restart, (WIDTH // 2 - 150, HEIGHT // 2))
