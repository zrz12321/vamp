# weapon_manager.py  (inside /Weapon directory)

from Weapon.axe import Axe
from Weapon.shuriken import Shuriken
from Weapon.burst import Burst
from Weapon.fireball import Fireball
from Weapon.gun import Gun


WEAPON_TYPES = {
    "axe": Axe,
    "shuriken": Shuriken,
    "burst": Burst,
    "fireball": Fireball,
    "gun": Gun,
}


class WeaponManager:
    def __init__(self, player):
        self.player = player
        self.weapons = []

    def give_weapon(self, weapon_name):
        if weapon_name not in WEAPON_TYPES:
            print(f"[WeaponManager] ERROR: Weapon '{weapon_name}' not found.")
            return

        weapon = WEAPON_TYPES[weapon_name](self.player)
        self.weapons.append(weapon)

        print("[WeaponManager] Equipped:", weapon_name)

    def update(self, enemies, xp_group):
        for w in self.weapons:
            w.update(enemies, xp_group)

    def draw(self, surface, ox, oy):
        for w in self.weapons:
            w.draw(surface, ox, oy)
