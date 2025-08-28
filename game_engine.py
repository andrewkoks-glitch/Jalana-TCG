from game_structures import Player, HeroCard, ItemCard, GameState
import random

class GameEngine:
    def __init__(self, player1: Player, player2: Player, item_deck: list):
        self.state = GameState(players=[player1, player2])
        self.item_deck = item_deck
        self.start_game()

    def start_game(self):
        # If item_deck has enough cards, draw 5 for each player; otherwise, keep their existing hand
        for player in self.state.players:
            if self.item_deck and len(self.item_deck) >= 5:
                player.hand = [self.item_deck.pop() for _ in range(5)]
            # else: keep the hand as set up externally
            player.mana = 0
            player.reset_turn_actions()

    def start_turn(self):
        player = self.state.players[self.state.current_turn]
        player.add_mana(6)
        player.reset_turn_actions()

    def act_with_hero(self, player_index: int, hero_index: int, action: str, ability_index: int = None):
        player = self.state.players[player_index]
        hero = player.heroes[hero_index]
        if not player.can_act(hero_index):
            return 'Hero already acted this turn.'
        if action == 'normal_attack':
            hero.energy += 1
            player.set_acted(hero_index)
            return f"{hero.name} performed a normal attack."
        elif action == 'ability' and ability_index is not None:
            ability = hero.abilities[ability_index]
            cost = ability.get('mana_cost', 0)
            if player.mana >= cost:
                player.mana -= cost
                hero.energy += 1
                player.set_acted(hero_index)
                return f"{hero.name} used ability: {ability['name']}"
            else:
                return 'Not enough mana.'
        elif action == 'ultimate':
            ult = hero.ultimate
            mana_cost = ult.get('mana_cost', 0)
            energy_cost = ult.get('energy_cost', 0)
            if player.mana >= mana_cost and hero.energy >= energy_cost:
                player.mana -= mana_cost
                hero.energy -= energy_cost
                player.set_acted(hero_index)
                return f"{hero.name} used ultimate: {ult['name']}"
            else:
                return 'Not enough mana or energy.'
        elif action == 'pass':
            player.set_acted(hero_index)
            return f"{hero.name} passed."
        else:
            return 'Invalid action.'

    def play_item_card(self, player_index: int, card_index: int):
        player = self.state.players[player_index]
        if 0 <= card_index < len(player.hand):
            card = player.hand.pop(card_index)
            player.add_mana(card.mana_gain)
            return f"Played item card: {card.name} for +{card.mana_gain} mana."
        return 'Invalid card index.'

    def end_turn(self):
        self.state.next_turn()
        self.start_turn()

    def check_victory(self):
        for i, player in enumerate(self.state.players):
            if all(hero.hp <= 0 for hero in player.heroes):
                return 1 - i  # Opponent wins
        return None
