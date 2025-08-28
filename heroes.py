from game_structures import HeroCard, StatusEffect, Frozen

class Andrey(HeroCard):
    def __init__(self):
        super().__init__("Andrey", hp=13, max_hp=13, class_type="Main Damage")

    def has_frozen(self, target):
        return any(isinstance(eff, Frozen) for eff in getattr(target, 'effects', []))

    def passive_bonus(self, target):
        # +1 bonus damage if target is Frozen
        return 1 if self.has_frozen(target) else 0

    def normal_attack(self, target):
        dmg = 2 + self.passive_bonus(target)
        target.take_damage(dmg)
        self.energy += 1
        print(f"Andrey attacks {target.name} for {dmg} damage. (Energy: {self.energy})")

    def ability(self, player, target):
        mana_cost = 2
        if player.mana < mana_cost:
            print(f"Not enough mana for Andrey's ability!")
            return
        player.mana -= mana_cost
        dmg = 3 + self.passive_bonus(target)
        target.take_damage(dmg)
        target.effects.append(Frozen(duration=2))
        self.energy += 1
        print(f"Andrey uses ability on {target.name}: {dmg} damage and Frozen for 2 turns. (Energy: {self.energy})")

    def ultimate(self, player, enemies):
        mana_cost = 3
        energy_cost = 3
        if player.mana < mana_cost or self.energy < energy_cost:
            print("Not enough mana or energy for Andrey's ultimate.")
            return
        player.mana -= mana_cost
        self.energy -= energy_cost
        for enemy in enemies:
            bonus = 2 if self.has_frozen(enemy) else 0
            dmg = 2 + bonus
            enemy.take_damage(dmg)
            enemy.effects.append(Frozen(duration=2))
            print(f"Andrey's ultimate hits {enemy.name} for {dmg} and applies Frozen (2 turns).")
