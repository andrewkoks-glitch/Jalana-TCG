import tkinter as tk
from tkinter import ttk, messagebox

# App state
decks = []
current_deck = {"heroes": [], "items": []}
volume = 50
brightness = 50

# --- Main Application Class ---
class TCGApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TCG Game")
        self.geometry("400x400")
        self.resizable(False, False)
        self.active_frame = None
        self.show_start_menu()

    def clear_frame(self):
        if self.active_frame:
            self.active_frame.destroy()
            self.active_frame = None

    def show_start_menu(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True)
        tk.Label(frame, text="Welcome to TCG!", font=("Arial", 18)).pack(pady=20)
        # Start Game only enabled if a deck is selected
        start_btn = tk.Button(frame, text="Start Game", width=20, command=self.show_game_loop)
        if not hasattr(self, 'selected_deck') or self.selected_deck is None:
            start_btn.config(state="disabled")
        start_btn.pack(pady=5)
        tk.Button(frame, text="Decks", width=20, command=self.show_deck_menu).pack(pady=5)
        tk.Button(frame, text="Settings", width=20, command=self.show_settings_menu).pack(pady=5)
        tk.Button(frame, text="Quit", width=20, command=self.quit).pack(pady=5)
        self.active_frame = frame

    def start_game(self):
        messagebox.showinfo("Game", "Game would start now! (Not implemented)")

    def show_deck_menu(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")
        tk.Label(frame, text="Your Decks", font=("Arial", 16)).pack(pady=10)
        for i, deck in enumerate(decks):
            deck_frame = tk.Frame(frame)
            deck_frame.pack(pady=2, fill="x", padx=40)
            tk.Label(deck_frame, text=f"Deck {i+1}").pack(side="left")
            tk.Button(deck_frame, text="Select", command=lambda d=deck: self.select_deck(d)).pack(side="right")
        tk.Button(frame, text="Create Deck", command=self.open_deck_builder).pack(pady=10)
        tk.Button(frame, text="Back", command=self.show_start_menu).pack(pady=10)
        self.active_frame = frame

    def open_deck_builder(self):
        builder = tk.Toplevel(self)
        builder.title("Deck Builder")
        builder.geometry("500x500")
        builder.resizable(False, False)

        # State for this builder
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

        # Hero and Item lists
        all_heroes = ["Warrior", "Mage", "Keira", "Healer"]
        all_items = ["Mana Potion", "Mana Crystal", "Elixir"]

        def update_list():
            for widget in scrollable.winfo_children():
                widget.destroy()
            if builder.tab.get() == "Heroes":
                for h in all_heroes:
                    btn = tk.Button(scrollable, text=h, width=30,
                        state=("disabled" if len(builder.selected_heroes) >= 3 or h in builder.selected_heroes else "normal"),
                        command=lambda name=h: add_to_deck("heroes", name))
                    btn.pack(pady=2)
            else:
                for i in all_items:
                    btn = tk.Button(scrollable, text=i, width=30,
                        state=("disabled" if len(builder.selected_items) >= 15 or i in builder.selected_items else "normal"),
                        command=lambda name=i: add_to_deck("items", name))
                    btn.pack(pady=2)
            counter_var.set(f"Heroes: {len(builder.selected_heroes)}/3    Items: {len(builder.selected_items)}/15")

        def add_to_deck(deck_type, name):
            if deck_type == "heroes":
                if len(builder.selected_heroes) < 3 and name not in builder.selected_heroes:
                    builder.selected_heroes.append(name)
            else:
                if len(builder.selected_items) < 15 and name not in builder.selected_items:
                    builder.selected_items.append(name)
            update_list()

        def save_deck():
            if len(builder.selected_heroes) != 3 or len(builder.selected_items) != 15:
                messagebox.showwarning("Deck Incomplete", "You need 3 heroes and 15 items.")
                return
            decks.append({"heroes": builder.selected_heroes.copy(), "items": builder.selected_items.copy()})
            messagebox.showinfo("Deck Saved", "Deck saved successfully!")
            builder.destroy()

        # Save and Cancel buttons
        btn_frame = tk.Frame(builder)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Save Deck", command=save_deck).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Cancel", command=builder.destroy).pack(side="left", padx=10)

        update_list()

    def select_deck(self, deck):
        global current_deck
        current_deck = deck
        self.selected_deck = deck
        messagebox.showinfo("Deck Selected", "Deck selected successfully!")
        self.show_start_menu()

    def create_new_deck(self):
        messagebox.showinfo("Deck Builder", "Deck builder not implemented in this skeleton.")

    def show_settings_menu(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True)
        tk.Label(frame, text="Settings", font=("Arial", 16)).pack(pady=10)

        # Volume slider
        tk.Label(frame, text="Volume").pack(pady=(10,0))
        vol_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", command=self.set_volume, length=250)
        vol_slider.set(volume)
        vol_slider.pack()

        # Brightness slider
        tk.Label(frame, text="Brightness").pack(pady=(10,0))
        bright_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", command=self.set_brightness, length=250)
        bright_slider.set(brightness)
        bright_slider.pack()

        # Back button
        tk.Button(frame, text="Back", command=self.show_start_menu).pack(pady=20)
        self.active_frame = frame

    def show_game_loop(self):
        self.clear_frame()
        frame = tk.Frame(self)
        frame.pack(expand=True)

        # Use selected deck for Player 1
        p1_deck = self.selected_deck if hasattr(self, 'selected_deck') and self.selected_deck else {"heroes": [], "items": []}
        # Dummy opponent deck
        dummy_heroes = ["Warrior", "Mage", "Healer"]
        dummy_items = ["Mana Potion"] * 15
        p2_deck = {"heroes": dummy_heroes, "items": dummy_items}

        tk.Label(frame, text="Game Loop (placeholder)", font=("Arial", 16)).pack(pady=10)
        tk.Label(frame, text="Player 1 Deck:").pack()
        tk.Label(frame, text=f"Heroes: {', '.join(p1_deck['heroes'])}").pack()
        tk.Label(frame, text=f"Items: {', '.join(p1_deck['items'])}").pack()
        tk.Label(frame, text="Opponent Deck:").pack(pady=(10,0))
        tk.Label(frame, text=f"Heroes: {', '.join(p2_deck['heroes'])}").pack()
        tk.Label(frame, text=f"Items: {', '.join(p2_deck['items'])}").pack()

        tk.Button(frame, text="Back", command=self.show_start_menu).pack(pady=10)
        self.active_frame = frame

    def set_volume(self, val):
        global volume
        volume = int(val)

    def set_brightness(self, val):
        global brightness
        brightness = int(val)

if __name__ == "__main__":
    app = TCGApp()
    app.mainloop()
