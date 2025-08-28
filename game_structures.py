

from dataclasses import dataclass, field
from typing import List

# --- Base Classes ---
class StatusEffect:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
    def on_apply(self, hero):
        pass
    def on_remove(self, hero):
        pass
    def modify_cost(self, cost):
        return cost
    def modify_damage_taken(self, dmg):
        return dmg

@dataclass
class HeroCard:
    def receive_heal(self, amount):
        # Some passives may boost healing
        bonus = 0
        if hasattr(self, "heal_bonus"):
            bonus = self.heal_bonus
        healed = min(self.max_hp - self.hp, amount + bonus)
        self.hp += healed
        print(f"{self.name} heals for {healed} (HP: {self.hp}/{self.max_hp})")
    def update_effects(self):
        new_effects = []
        for eff in self.effects:
            eff.duration -= 1
            if eff.duration > 0:
                new_effects.append(eff)
            else:
                eff.on_remove(self)
                print(f"{self.name} is no longer affected by {eff.name}.")
        self.effects = new_effects
    name: str
    hp: int
    max_hp: int
    class_type: str  # e.g., 'Main damage', 'Sub damage', 'Sustain', 'Support'
    energy: int = 0
    normal_attack: str = ""
    abilities: list = field(default_factory=list)  # List of dicts or objects for abilities
    ultimate: dict = field(default_factory=dict)   # Dict/object for ultimate ability
    passives: list = field(default_factory=list)   # List of dicts or objects for passives
    effects: list = field(default_factory=list)    # List of StatusEffect objects
    shield: int = 0
    alive: bool = True

    def take_damage(self, amount):
        # Check vulnerability & other effects
        for eff in self.effects:
            amount = eff.modify_damage_taken(amount)

        # Apply shield first
        if self.shield > 0 and amount > 0:
            absorbed = min(amount, self.shield)
            self.shield -= absorbed
            amount -= absorbed
            print(f"{self.name}'s shield absorbed {absorbed} damage!")

        # Apply leftover damage
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            print(f"{self.name} has been defeated!")

class Summon:
    def __init__(self, name, duration, action):
        self.name = name
        self.duration = duration  # number of turns it lasts
        self.action = action      # function(player, opponent) to run at turn start

    def on_turn_start(self, player, opponent):
        print(f"{self.name} activates!")
        self.action(player, opponent)
        self.duration -= 1
        if self.duration <= 0:
            print(f"{self.name} disappears!")
            return False  # remove from board
        return True       # still alive

# --- Subclasses ---
class Keira(HeroCard):
    def __init__(self):
        super().__init__("Keira", hp=15, max_hp=15, class_type="Sustain")
        self.heal_bonus = 1  # passive: receives +1 HP from all heals

    def ability(self, player):
        mana_cost = 2
        if player.mana < mana_cost:
            print(f"{player.name} does not have enough mana for Keira's ability!")
            return
        player.mana -= mana_cost
        print("Keira uses Group Heal! All allies recover 2 HP.")
        for ally in player.heroes:
            if ally.alive:
                ally.receive_heal(2)

    def ultimate(self, player):
        mana_cost = 4
        energy_cost = 3
        if player.mana < mana_cost or self.energy < energy_cost:
            print("Not enough mana or energy for Keira's ultimate.")
            return
        player.mana -= mana_cost
        self.energy -= energy_cost
        print("Keira summons Pink Satellite! 🌸")
        satellite = Summon(
            "Pink Satellite",
            duration=3,
            action=lambda p, o: [ally.receive_heal(1) for ally in p.heroes if ally.alive]
        )
        player.summons.append(satellite)

class Frozen(StatusEffect):
    def __init__(self, duration=2):
        super().__init__("Frozen", duration)
    def modify_cost(self, cost):
        return cost + 1

class Vulnerability(StatusEffect):
    def __init__(self, duration=2):
        super().__init__("Vulnerability", duration)
    def modify_damage_taken(self, dmg):
        if dmg > 0:
            return dmg + 1
        return dmg

class Shield(StatusEffect):
    def __init__(self, amount):
        super().__init__("Shield", duration=999)
        self.amount = amount
    def on_apply(self, hero):
        hero.shield += self.amount
    def on_remove(self, hero):
        hero.shield -= self.amount

@dataclass
class ItemCard:
    name: str
    mana_gain: int
    # Optional: buffs/debuffs can be added later

@dataclass
class Player:
    name: str
    heroes: List[HeroCard] = field(default_factory=list)  # 3 HeroCards
    hand: List[ItemCard] = field(default_factory=list)
    mana: int = 0
    max_mana: int = 20
    turn_actions: List[bool] = field(default_factory=lambda: [False, False, False])  # Track if each hero has acted this turn
    summons: list = field(default_factory=list)  # List of Summon objects

    def add_mana(self, amount: int):
        self.mana = min(self.mana + amount, self.max_mana)

    def reset_turn_actions(self):
        self.turn_actions = [False, False, False]

    def can_act(self, hero_index: int) -> bool:
        return not self.turn_actions[hero_index]

    def set_acted(self, hero_index: int):
        self.turn_actions[hero_index] = True

# Example Summons
def fire_elemental_action(player, opponent):
    opponent.heroes[0].hp = max(0, opponent.heroes[0].hp - 2)

def healing_spirit_action(player, opponent):
    lowest = min(player.heroes, key=lambda h: h.hp)
    lowest.hp = min(lowest.max_hp, lowest.hp + 3)

fire_elemental = Summon("Fire Elemental", duration=3, action=fire_elemental_action)
healing_spirit = Summon("Healing Spirit", duration=2, action=healing_spirit_action)

@dataclass
class GameState:
    players: List[Player]
    current_turn: int = 0  # 0 for Player 1, 1 for Player 2

    def next_turn(self):
        self.current_turn = 1 - self.current_turn
        self.players[self.current_turn].add_mana(6)
