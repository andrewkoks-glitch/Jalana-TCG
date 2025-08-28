from game_structures import Player, HeroCard
try:
    from game_structures import Keira
except ImportError:
    Keira = None
try:
    from heroes import Andrey
except ImportError:
    Andrey = None
try:
    from items import SwearJar, Luna
except ImportError:
    SwearJar = None
    Luna = None
import tkinter as tk
from tkinter import ttk, messagebox

# Hero and item lists (add new cards here)
ALL_HEROES = ["Keira", "Andrey", "Warrior", "Mage", "Healer"]
ALL_ITEMS = ["Mana Potion", "Mana Crystal", "Elixir", "Swear Jar", "Luna"]

class GameUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("TCG Game")
        self.root.geometry("420x420")
        self.decks = []
        self.selected_deck = None
        self.volume = 50
        self.brightness = 50
        self.show_start_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_start_menu(self):
        self.clear_window()
        frame = tk.Frame(self.root)
        frame.pack(expand=True)
        tk.Label(frame, text="Welcome to TCG!", font=("Arial", 18)).pack(pady=20)
        tk.Button(frame, text="Start Game", width=20, command=self.start_actual_game).pack(pady=5)
        tk.Button(frame, text="Decks", width=20, command=self.open_deck_menu).pack(pady=5)
        tk.Button(frame, text="Settings", width=20, command=self.open_settings_menu).pack(pady=5)
        tk.Button(frame, text="Quit", width=20, command=self.root.quit).pack(pady=5)

    def start_actual_game(self):
        # Check for selected deck
        if not self.selected_deck:
            messagebox.showwarning("No Deck Selected", "Please build or select a deck before starting the game.")
            return
        # Hide start menu
        self.clear_window()
        # Prepare player decks
        hero_names = self.selected_deck["heroes"]
        item_names = self.selected_deck["items"]
        # Instantiate hero objects
        p1_heroes = []
        for name in hero_names:
            if name == "Keira" and Keira:
                p1_heroes.append(Keira())
            elif name == "Andrey" and Andrey:
                p1_heroes.append(Andrey())
            else:
                p1_heroes.append(HeroCard(name, 15, 15, "Unknown"))
        # For now, items are just names; you can expand to real objects if needed
        player1 = Player("Player 1", p1_heroes, [])
        # Dummy Player 2 (AI or placeholder deck)
        p2_heroes = [HeroCard("Assassin", 15, 15, "Unknown"), HeroCard("Tank", 15, 15, "Unknown"), HeroCard("Healer", 15, 15, "Unknown")]
        player2 = Player("Player 2", p2_heroes, [])
        # Import GameEngine here to avoid circular import
        from game_engine import GameEngine
        # For now, item_deck is empty or can be built from item_names
        item_deck = []
        self.engine = GameEngine(player1, player2, item_deck)
        # Show the battle window UI (can be improved to sync with engine state)
        self.open_battle_window()

    def open_battle_window(self):
        # Main battlefield window (replace previous placeholder)
        self.clear_window()
        self.battle_frame = tk.Frame(self.root)
        self.battle_frame.pack(fill="both", expand=True)

        # Battlefield layout frames
        self.enemy_frame = tk.Frame(self.battle_frame)
        self.enemy_frame.pack(side="top", pady=10)
        self.status_frame = tk.Frame(self.battle_frame)
        self.status_frame.pack(side="top", pady=2)
        self.player_frame = tk.Frame(self.battle_frame)
        self.player_frame.pack(side="bottom", pady=10)
        self.item_frame = tk.Frame(self.battle_frame)
        self.item_frame.pack(side="bottom", pady=5)
        self.target_frame = tk.Frame(self.battle_frame)
        self.target_frame.pack(side="bottom", pady=5)

        self.refresh_battlefield()

    def refresh_battlefield(self):
        # Clear all battlefield frames
        for frame in [self.enemy_frame, self.status_frame, self.player_frame, self.item_frame, self.target_frame]:
            for widget in frame.winfo_children():
                widget.destroy()

        engine = self.engine
        state = engine.state
        p1 = state.players[0]
        p2 = state.players[1]
        turn = state.current_turn

        # --- Enemy Side ---
        tk.Label(self.enemy_frame, text="Enemy Heroes", font=("Arial", 12)).pack()
        for idx, hero in enumerate(p2.heroes):
            hero_str = f"{hero.name} | HP: {hero.hp}/{hero.max_hp} | Energy: {hero.energy}"
            if not hero.alive:
                hero_str += " [DEFEATED]"
            effs = ', '.join([eff.name for eff in getattr(hero, 'effects', [])])
            if effs:
                hero_str += f" | Effects: {effs}"
            tk.Label(self.enemy_frame, text=hero_str, fg=("gray" if not hero.alive else "black"), relief="ridge", width=40).pack(pady=2)

        # --- Status Bar ---
        tk.Label(self.status_frame, text=f"Your Mana: {p1.mana}    |    Turn: {'You' if turn==0 else 'Enemy'}", font=("Arial", 11)).pack()

        # --- Player Side ---
        tk.Label(self.player_frame, text="Your Heroes", font=("Arial", 12)).pack()
        for idx, hero in enumerate(p1.heroes):
            hero_str = f"{hero.name} | HP: {hero.hp}/{hero.max_hp} | Energy: {hero.energy}"
            if not hero.alive:
                hero_str += " [DEFEATED]"
            effs = ', '.join([eff.name for eff in getattr(hero, 'effects', [])])
            if effs:
                hero_str += f" | Effects: {effs}"
            row = tk.Frame(self.player_frame)
            row.pack(pady=2)
            tk.Label(row, text=hero_str, fg=("gray" if not hero.alive else "black"), relief="ridge", width=40).pack(side="left")
            # Action buttons
            if hero.alive and turn == 0 and p1.can_act(idx):
                btns = tk.Frame(row)
                btns.pack(side="left", padx=5)
                tk.Button(btns, text="Attack", command=lambda i=idx: self.hero_action(i, 'normal_attack')).pack(side="left")
                tk.Button(btns, text="Ability", state=("normal" if hasattr(hero, 'ability') and p1.mana >= 2 else "disabled"), command=lambda i=idx: self.hero_action(i, 'ability')).pack(side="left")
                tk.Button(btns, text="Ultimate", state=("normal" if hasattr(hero, 'ultimate') and p1.mana >= 3 and hero.energy >= 3 else "disabled"), command=lambda i=idx: self.hero_action(i, 'ultimate')).pack(side="left")

        # --- Item Hand ---
        tk.Label(self.item_frame, text="Your Items", font=("Arial", 11)).pack()
        for idx, item in enumerate(p1.hand):
            tk.Button(self.item_frame, text=f"{item.name} (+{item.mana_gain} mana)", command=lambda i=idx: self.play_item(i)).pack(side="left", padx=2)

        # --- Target Selection (populated as needed) ---
        # This will be filled by self.show_targets() when an action needs a target

    def hero_action(self, hero_idx, action):
        # For actions that require a target, show target selection
        if action in ('normal_attack', 'ability'):
            self.show_targets(hero_idx, action)
        else:
            # Ultimate: may be AoE or not require target
            result = self.engine.act_with_hero(0, hero_idx, action)
            self.refresh_battlefield()

    def show_targets(self, hero_idx, action):
        # Clear target frame
        for widget in self.target_frame.winfo_children():
            widget.destroy()
        # For now, attacks/abilities target enemy heroes
        p2 = self.engine.state.players[1]
        for idx, hero in enumerate(p2.heroes):
            if not hero.alive:
                continue
            btn = tk.Button(self.target_frame, text=f"Target {hero.name}", command=lambda i=idx: self.resolve_target(hero_idx, action, i))
            btn.pack(side="left", padx=2)

    def resolve_target(self, hero_idx, action, target_idx):
        # Call the game logic for the action
        # For now, only normal_attack and ability are supported
        # You can expand this to call the actual hero's method if needed
        # Here, we just call act_with_hero for normal_attack
        if action == 'normal_attack':
            result = self.engine.act_with_hero(0, hero_idx, 'normal_attack')
        elif action == 'ability':
            # You can expand to pass ability index if needed
            result = self.engine.act_with_hero(0, hero_idx, 'ability', ability_index=0)
        # Hide target selection
        for widget in self.target_frame.winfo_children():
            widget.destroy()
        self.refresh_battlefield()

    def play_item(self, item_idx):
        result = self.engine.play_item_card(0, item_idx)
        self.refresh_battlefield()

    def open_deck_menu(self):
        deck_win = tk.Toplevel(self.root)
        deck_win.title("Decks")
        deck_win.geometry("400x400")
        tk.Label(deck_win, text="Your Decks", font=("Arial", 16)).pack(pady=10)
        for i, deck in enumerate(self.decks):
            deck_frame = tk.Frame(deck_win)
            deck_frame.pack(pady=2, fill="x", padx=40)
            tk.Label(deck_frame, text=f"Deck {i+1}").pack(side="left")
            tk.Button(deck_frame, text="Select", command=lambda d=deck: self.select_deck(d)).pack(side="right")
        tk.Button(deck_win, text="Create Deck", command=lambda: self.open_deck_builder(deck_win)).pack(pady=10)
        tk.Button(deck_win, text="Back", command=deck_win.destroy).pack(pady=10)

    def select_deck(self, deck):
        self.selected_deck = deck
        messagebox.showinfo("Deck Selected", "Deck selected successfully!")

    def open_deck_builder(self, parent):
        builder = tk.Toplevel(parent)
        builder.title("Deck Builder")
        builder.geometry("520x520")
        builder.selected_heroes = []
        builder.selected_items = []
        builder.tab = tk.StringVar(value="Heroes")

        # Top toggle buttons
        toggle_frame = tk.Frame(builder)
        toggle_frame.pack(fill="x", pady=5)
        def show_heroes(): builder.tab.set("Heroes"); update_list()
        def show_items(): builder.tab.set("Items"); update_list()
        tk.Button(toggle_frame, text="Heroes", command=show_heroes, width=10).pack(side="left", padx=10)
        tk.Button(toggle_frame, text="Items", command=show_items, width=10).pack(side="left")

        # Counters
        counter_var = tk.StringVar()
        counter_label = tk.Label(builder, textvariable=counter_var)
        counter_label.pack(pady=2)

        # Deck display (removable)
        deck_display = tk.Frame(builder)
        deck_display.pack(side="right", fill="y", padx=10)
        deck_label = tk.Label(deck_display, text="Current Deck:")
        deck_label.pack()
        deck_cards_frame = tk.Frame(deck_display)
        deck_cards_frame.pack()

        # Scrollable list
        list_frame = tk.Frame(builder)
        list_frame.pack(expand=True, fill="both", padx=10, pady=5)
        canvas = tk.Canvas(list_frame)
        scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable = tk.Frame(canvas)
        scrollable.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        def update_deck_display():
            for widget in deck_cards_frame.winfo_children():
                widget.destroy()
            # Show heroes (unique)
            for h in builder.selected_heroes:
                btn = tk.Button(deck_cards_frame, text=f"{h}", width=18, command=lambda name=h: remove_from_deck("heroes", name))
                btn.pack(pady=1)
            # Show items (with counts)
            item_counts = {}
            for i in builder.selected_items:
                item_counts[i] = item_counts.get(i, 0) + 1
            for i, count in item_counts.items():
                btn = tk.Button(deck_cards_frame, text=f"{i} x{count}", width=18, command=lambda name=i: remove_from_deck("items", name))
                btn.pack(pady=1)

        def update_list():
            for widget in scrollable.winfo_children():
                widget.destroy()
            if builder.tab.get() == "Heroes":
                for h in ALL_HEROES:
                    btn = tk.Button(scrollable, text=h, width=30,
                        state=("disabled" if len(builder.selected_heroes) >= 3 or h in builder.selected_heroes else "normal"),
                        command=lambda name=h: add_to_deck("heroes", name))
                    btn.pack(pady=2)
            else:
                # Count each item
                item_counts = {}
                for i in builder.selected_items:
                    item_counts[i] = item_counts.get(i, 0) + 1
                for i in ALL_ITEMS:
                    count = item_counts.get(i, 0)
                    btn = tk.Button(scrollable, text=f"{i} ({count}/4)", width=30,
                        state=("disabled" if len(builder.selected_items) >= 15 or count >= 4 else "normal"),
                        command=lambda name=i: add_to_deck("items", name))
                    btn.pack(pady=2)
            counter_var.set(f"Heroes: {len(builder.selected_heroes)}/3    Items: {len(builder.selected_items)}/15")
            update_deck_display()

        def add_to_deck(deck_type, name):
            if deck_type == "heroes":
                if len(builder.selected_heroes) < 3 and name not in builder.selected_heroes:
                    builder.selected_heroes.append(name)
            else:
                # Count how many copies of this item
                count = builder.selected_items.count(name)
                if len(builder.selected_items) < 15 and count < 4:
                    builder.selected_items.append(name)
            update_list()

        def remove_from_deck(deck_type, name):
            if deck_type == "heroes":
                if name in builder.selected_heroes:
                    builder.selected_heroes.remove(name)
            else:
                if name in builder.selected_items:
                    builder.selected_items.remove(name)
            update_list()

        def save_deck():
            if len(builder.selected_heroes) != 3 or len(builder.selected_items) != 15:
                messagebox.showwarning("Deck Incomplete", "You need 3 heroes and 15 items.")
                return
            self.decks.append({"heroes": builder.selected_heroes.copy(), "items": builder.selected_items.copy()})
            messagebox.showinfo("Deck Saved", "Deck saved successfully!")
            builder.destroy()

        # Save and Cancel buttons
        btn_frame = tk.Frame(builder)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Save Deck", command=save_deck).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=builder.destroy).pack(side="left", padx=10)

        update_list()

    def open_settings_menu(self):
        settings = tk.Toplevel(self.root)
        settings.title("Settings")
        settings.geometry("350x250")
        tk.Label(settings, text="Settings", font=("Arial", 16)).pack(pady=10)
        tk.Label(settings, text="Volume").pack(pady=(10,0))
        vol_slider = tk.Scale(settings, from_=0, to=100, orient="horizontal", command=self.set_volume, length=250)
        vol_slider.set(self.volume)
        vol_slider.pack()
        tk.Label(settings, text="Brightness").pack(pady=(10,0))
        bright_slider = tk.Scale(settings, from_=0, to=100, orient="horizontal", command=self.set_brightness, length=250)
        bright_slider.set(self.brightness)
        bright_slider.pack()
        tk.Button(settings, text="Back", command=settings.destroy).pack(pady=20)

    def set_volume(self, val):
        self.volume = int(val)

    def set_brightness(self, val):
        self.brightness = int(val)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    GameUI().run()
