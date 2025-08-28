from game_structures import ItemCard, Summon

class SwearJar(ItemCard):
    def __init__(self):
        super().__init__("Swear Jar", mana_gain=1)
    def play(self, player, opponent):
        if opponent.mana >= 2:
            opponent.mana -= 2
        else:
            opponent.mana = 0
        print(f"Swear Jar played! {opponent.name} loses 2 mana.")

class LunaSummon(Summon):
    def __init__(self):
        super().__init__("Luna", duration=3, action=self.luna_effect)
    def luna_effect(self, player, opponent):
        player.add_mana(1)
        print(f"Luna grants +1 mana to {player.name}!")

class Luna(ItemCard):
    def __init__(self):
        super().__init__("Luna", mana_gain=3)
    def play(self, player, opponent):
        luna = LunaSummon()
        player.summons.append(luna)
        print(f"Luna is summoned for 3 turns!")
