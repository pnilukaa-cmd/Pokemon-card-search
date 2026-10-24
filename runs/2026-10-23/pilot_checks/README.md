# Pilot checks, 2026-10-23

Four AI changes, each measured on the decks it touches before it was turned
on (or taken back out). All against the 95-deck field, 200 games per
opponent, paired on the same seeds within a tag; `paired.py A.json B.json`
prints B − A.

**switch_pick** (on, a569a0d). Switch was played the moment it was drawn,
into the healthiest Benched Pokémon. It now waits until a Benched Pokémon
does more this turn than the Active.
- Tag hp0. `X_user` is the submitted Snorlax list: +12.39 ± 0.71.
  `C_base` is the first Chesnaught build: +2.29 ± 0.46.
- `F_*`: 8 field decks with Switch, +0.28 to +5.83, none worse.
- The commit also has an Asleep or Paralyzed Active rank 0 for Sky
  Transport and the switch-in Abilities. That is a correctness fix with
  its own test; the title of f01e13e mentions it, but it went out here.

**engine_first** (on, f01e13e). Rare Candy, evolution and Pokémon searches
go first to an evolved Pokémon whose passive Ability covers your whole side,
while none is in play.
- Tag hp1. `E_*`: 8 field decks, with Basic engines included as well.
  −1.50 on Raging Bolt (Latias ex), noise elsewhere.
- `R_*`: restricted to evolved engines. The Exeggutor list +2.27 ± 0.44,
  Mew / Bastiodon +0.82, Raging Bolt +0.04 (no longer touched).

**overflow_attach** (taken out, a569a0d). With nobody short of an attack,
put the manual attachment where one more Energy adds damage, HP or
Energy-counted retaliation.
- Tag hp0, on four Chesnaught lists (`chesnaught_screens/results/*__overflow_attach_*`).
- Setting 2: −0.38 to +0.76. Setting 3: −2.49 to +0.52.

**self_attach_spare** (never committed). Skip Teal Dance when the only Energy
in hand is wanted elsewhere.
- Tag hp2. `A_*`: the two field decks with Teal Mask Ogerpon ex, 0.00 and
  −0.28.
- The Exeggutor and Chesnaught lists: −0.50, +0.02.

Tags: hp0 = be34d64, hp1 = a569a0d, hp2 = f01e13e.
