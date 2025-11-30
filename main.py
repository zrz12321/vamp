import pygame
import random

from characters import CHARACTER_LIST
from player import Player
from enemy import BasicEnemy, FastEnemy, TankEnemy
from map import Map
from utils import WIDTH, HEIGHT, screen, WORLD_WIDTH, WORLD_HEIGHT, Camera
from weapon_manager import WeaponManager
from xp_orb import XPOrb
from game_manager import GameManager

pygame.init()
pygame.display.set_caption("Pixel Survivors - Character Select + Camera World")
clock = pygame.time.Clock()


# --------------------------------------------------------
# MINIMAP DRAW FUNCTION
# --------------------------------------------------------
def draw_minimap(player, enemies, surface):
    MAP_W, MAP_H = 180, 180
    margin = 20

    rect = pygame.Rect(surface.get_width() - MAP_W - margin,
                       margin,
                       MAP_W, MAP_H)

    # background box
    pygame.draw.rect(surface, (10, 10, 10), rect)
    pygame.draw.rect(surface, (255, 255, 255), rect, 2)

    # scale factors
    sx = MAP_W / WORLD_WIDTH
    sy = MAP_H / WORLD_HEIGHT

    # --- Player dot ---
    player.draw_minimap(surface, rect)

    # --- Enemy dots ---
    for e in enemies:
        ex = int(e.rect.centerx * sx)
        ey = int(e.rect.centery * sy)
        pygame.draw.circle(surface, (255, 0, 0),
                           (rect.x + ex, rect.y + ey), 2)


# --------------------------------------------------------
# CHARACTER SELECT MENU
# --------------------------------------------------------
def choose_character():
    selecting = True
    font = pygame.font.Font(None, 60)
    small_font = pygame.font.Font(None, 40)

    buttons = []
    y = 180

    for name in CHARACTER_LIST:
        rect = pygame.Rect(WIDTH // 2 - 250, y, 500, 70)
        buttons.append((name, rect))
        y += 100

    while selecting:
        screen.fill((25, 25, 40))
        title = font.render("Choose Your Character", True, (255, 255, 120))
        screen.blit(title, (WIDTH // 2 - 260, 60))

        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True

        for name, rect in buttons:
            hovered = rect.collidepoint(mouse_pos)

            pygame.draw.rect(screen, (60, 60, 90), rect)
            pygame.draw.rect(screen, (255, 255, 120) if hovered else (120, 120, 120), rect, 4)

            txt = small_font.render(name, True, (255, 255, 255))
            screen.blit(txt, txt.get_rect(center=rect.center))

            desc = CHARACTER_LIST[name].get("description", "")
            if desc:
                desc_txt = small_font.render(desc, True, (200, 200, 200))
                screen.blit(desc_txt, (rect.x + 10, rect.y + 45))

            if hovered and mouse_click:
                return name

        pygame.display.flip()
        clock.tick(60)


# --------------------------------------------------------
# CREATE NEW GAME
# --------------------------------------------------------
def create_game():
    chosen_name = choose_character()
    char_data = CHARACTER_LIST[chosen_name]

    # Create player with character stats
    player = Player(
        WORLD_WIDTH // 2,
        WORLD_HEIGHT // 2,
        hp=char_data["hp"],
        speed=char_data["speed"],
        color=char_data["color"],
    )
    player.base_damage = char_data["damage"]
    player.base_range = char_data["range"]

    # Weapon manager + starting weapon
    weapon_manager = WeaponManager(player)
    weapon_manager.give_weapon(char_data["weapon"])

    # Game manager
    game_manager = GameManager(weapon_manager)

    # Other game systems
    enemies = pygame.sprite.Group()
    xp_orbs = pygame.sprite.Group()
    camera = Camera()

    # Random map
    map_type = random.choice(["forest", "desert", "graveyard"])
    seed = random.randint(0, 999999)
    game_map = Map(map_type=map_type, seed=seed)
    print(f"Loaded map: {map_type} (seed {seed})")

    return player, weapon_manager, game_manager, enemies, xp_orbs, camera, game_map


# --------------------------------------------------------
# MAIN LOOP
# --------------------------------------------------------
player, weapon_manager, game_manager, enemies, xp_orbs, camera, game_map = create_game()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    mouse_clicked = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_clicked = True

        if event.type == pygame.KEYDOWN:
            # ESC only opens menu when XP upgrade is ready
            if event.key == pygame.K_ESCAPE:
                if player.has_level_up_ready() and not game_manager.show_upgrade and not game_manager.game_over:
                    game_manager.show_upgrade = True

            # Restart after game over
            if game_manager.game_over and event.key == pygame.K_r:
                player, weapon_manager, game_manager, enemies, xp_orbs, camera, game_map = create_game()

    # ------------------ UPGRADE MENU ------------------
    if game_manager.show_upgrade and mouse_clicked:
        choice = game_manager.check_mouse_click(mouse_pos)
        if choice == 1:
            player.speed += 0.5
        elif choice == 2:
            player.base_damage += 5
        elif choice == 3:
            player.base_range += 20

        if choice in (1, 2, 3):
            player.finish_level_up()
            game_manager.show_upgrade = False

    # ------------------ GAME UPDATE ------------------
    if not game_manager.show_upgrade and not game_manager.game_over:
        player.update()
        weapon_manager.update(enemies, xp_orbs)

        for enemy in list(enemies):
            enemy.update(player)
            enemy.handle_death(xp_orbs)

        for orb in xp_orbs:
            orb.update(player)

        camera.update(player.rect.centerx, player.rect.centery)
        game_manager.update(player, enemies, xp_orbs, camera)

    # ------------------ DRAW ------------------
    ox, oy = camera.x, camera.y

    # Map
    game_map.draw_background(screen, ox, oy)
    game_map.draw_decorations(screen, ox, oy)

    # Entities
    for enemy in enemies:
        enemy.draw(screen, ox, oy)

    for orb in xp_orbs:
        orb.draw(screen, ox, oy)

    player.draw(screen, ox, oy)
    weapon_manager.draw(screen, ox, oy)

    # Minimap (added back!)
    draw_minimap(player, enemies, screen)

    # UI
    game_manager.draw(player, mouse_pos)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
