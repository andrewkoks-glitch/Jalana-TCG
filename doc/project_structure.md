# Project Structure

```
/doc
    project_structure.md
    game_rules.md
/game_structures.py
/game_engine.py
/game_ui.py
/tcg_app.py
/main.py
/templates/ (if using Flask)
```

- **game_structures.py**: Core data classes (HeroCard, ItemCard, Player, Summon, StatusEffect, etc.)
- **game_engine.py**: Game logic and turn management (for CLI or backend logic)
- **game_ui.py**: Tkinter-based graphical user interface for the game
- **tcg_app.py**: Alternative or experimental UI (if present)
- **main.py**: Entry point for CLI or demo
- **/doc**: Documentation files
- **/templates**: HTML templates (if using Flask for web UI)

## Notes
- All class dependencies are ordered so subclasses are defined after their base classes.
- Decks, settings, and game state are managed in-memory for now.
- The UI can be run with `python game_ui.py`.
