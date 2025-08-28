from game_structures import Player, HeroCard, ItemCard
from game_engine import GameEngine

def game_loop(player1, player2):
	# Simple loop for demonstration; replace with real input/logic as needed
	engine = GameEngine(player1, player2, item_deck=[])
	engine.state.players[0].mana = 6
	engine.state.players[1].mana = 6
	print('Game started!')
	turn = 0
	while True:
		current_player = engine.state.players[engine.state.current_turn]
		print(f"\n{current_player.name}'s turn. Mana: {current_player.mana}")
		# For demo, just pass with all heroes
		for i, hero in enumerate(current_player.heroes):
			if current_player.can_act(i):
				print(engine.act_with_hero(engine.state.current_turn, i, 'pass'))
		winner = engine.check_victory()
		if winner is not None:
			print(f"{engine.state.players[winner].name} wins!")
			break
		engine.end_turn()

def main():
	# Create some heroes
	hero1 = HeroCard("Warrior", 20, 20, "Main Damage")
	hero2 = HeroCard("Mage", 15, 15, "Sub Damage")
	hero3 = HeroCard("Healer", 18, 18, "Support")

	hero4 = HeroCard("Assassin", 16, 16, "Main Damage")
	hero5 = HeroCard("Tank", 25, 25, "Sustain")
	hero6 = HeroCard("Cleric", 18, 18, "Support")

	# Create some items
	items_p1 = [ItemCard("Mana Potion", 3), ItemCard("Mana Potion", 3)]
	items_p2 = [ItemCard("Mana Crystal", 4), ItemCard("Mana Potion", 2)]

	# Create players
	player1 = Player("Player 1", [hero1, hero2, hero3], items_p1)
	player2 = Player("Player 2", [hero4, hero5, hero6], items_p2)

	# Start game loop
	game_loop(player1, player2)

if __name__ == "__main__":
	main()
