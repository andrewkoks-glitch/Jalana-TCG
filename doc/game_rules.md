# Jalana TCG Game Rules

## Players
- 2 players: Player 1 and Player 2
- Each player has:
  - 3 Hero Cards (always on the board)
  - A hand of Item Cards (used for mana)
  - Mana pool (starts at 0, +6 per turn, capped at 20)

## Turn Structure
- Players alternate turns
- At the start of your turn:
  - Gain +6 mana (max 20)
  - All summons activate their effects
  - All status effects on heroes update (duration decreases, effects may expire)
- Each hero can act once per turn:
  - Normal Attack (0 mana, +1 energy)
  - Ability (costs mana, +1 energy)
  - Ultimate (costs mana + energy)
  - Pass/Skip
- Item cards can be played from hand for extra mana
- End turn, next player starts

## Victory
- If all 3 opponent heroes’ HP = 0, you win

## Card Types
### HeroCard
- name, hp, max_hp, class_type (Main damage, Sub damage, Sustain, Support)
- energy (builds up from actions)
- normal_attack (free, +1 energy)
- abilities (cost mana, + energy)
- ultimate (cost mana + energy)
- passives (constant or conditional effects)
- effects (status effects)
- shield (for Shield effect)

### ItemCard
- name
- mana_gain
- (Optional: buffs/debuffs in future)

### Summon
- Created by item cards or hero abilities
- Stays on board for a set duration
- Activates automatically at start of your turn

### StatusEffect
- Can be attached to a HeroCard
- Has a name, duration, and effect hooks (on_apply, on_remove, modify_cost, modify_damage_taken)

## Decks
- Each deck: 3 heroes, 15 items
- Decks are created and selected in the UI

## UI Navigation
- Start Menu: Start Game, Decks, Settings, Quit
- Deck Menu: View/select/create decks
- Deck Builder: Pick 3 heroes, 15 items
- Settings: Volume, Brightness
- Game only starts after deck selection
