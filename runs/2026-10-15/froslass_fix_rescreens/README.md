# Froslass re-screens after the Freezing Shroud fix, 2026-10-15

Asked: "why is Froslass hitting my own Pokémon a negative, when Munkidori
can move those counters to their Bench?"

Answering it found that Freezing Shroud was broken. It put one counter on
one Pokémon (in practice its owner's Munkidori) instead of one on every
Pokémon with an Ability on both sides. It was fixed in 31176bf, and the
Froslass comparisons were re-run here on tag fz1 (93 decks, 200 games;
1000 for the confirmation).

**Lists:**
- `U_user`, `U_fros22`, `U_fros0`: the submitted list with 3-3, 2-2 and no
  Froslass.
- `U_dark`, `U_dark_fros0`: the same with 7 Darkness Energy, so more
  Munkidori can use Adrena-Brain.
- `s5_candy`, `K_fros22`, `K_fros33`: the recommended list with Froslass
  added back.
- `K_dark*`: the recommended list with more Darkness, with and without
  Froslass.
- `F_pure*`: a Froslass build with Munkidori as its only Ability Pokémon.

**Scripts:**
- `flow.py LIST N`: Freezing Shroud counters on each side, Adrena-Brain
  counters moved, and own Pokémon Knocked Out at checkup, per game.
- `munkiopp.py LIST N`: Munkidori in play with Darkness Energy, against
  Adrena-Brain uses.

Write-up: `decks/alakazam_munkidori_strange_hacking.md`, under "What the
measurements changed".
