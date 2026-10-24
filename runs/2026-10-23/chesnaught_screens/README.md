# Chesnaught / Meganium screens, 2026-10-23

A build on request: Chesnaught and Meganium, with Brambleghast and Alolan
Exeggutor considered for Chesnaught's low HP and enough Energy on the
board. Write-up: `decks/chesnaught_meganium_wild_growth.md`.

All against the 95-deck field, paired on the same seeds within a tag.
Screens are 200 games per opponent; the confirmation is 1000.

**Tags:**
- `hp0`: be34d64. HP Abilities fixed; Teal Dance attaches before it draws.
- `hp1`: a569a0d. Switch waits for a better attacker.
- `hp2`: f01e13e. Rare Candy and evolution go to the engine first.

**Rounds** (each paired against the best list of the round before):
- `c1_` from `C_base` (hp0). `c1_*__overflow_attach_*` are the overflow
  knob runs (see `../pilot_checks`).
- `c2_` from `c1_boss0` (hp1).
- `c3_` from `c3_base` (hp1). `c3_noches*` is the Exeggutor branch.
- `c4_` from `c4_base` = `c3_shaymin0` (hp2). `n4_` from `c4_noches`.
- `c5_` from `c4_base` (hp2). Best: `c5_g`, the final list.
- `n5_` from `c4_noches` (hp2). Best: `n5_b`, the Exeggutor version.
- `c6_` from `c5_g` (hp2). Nothing kept.
- **Confirmation:** 1000 games on hp2 for `C_base`, `c5_g` and `n5_b`.

**Scripts:**
- `variant.py BASE OUT 'Card SET NUM:+n' ...` writes a variant that stays at 60.
- `boardgame.py LIST OPP SEED [knobs]` plays one verbose game and prints
  your board each turn, Energy and HP left. It found Teal Dance spending
  the only Energy in hand.
- `energy_curve.py` (repo root) gave the Energy-on-board and Meganium-timing
  numbers.
