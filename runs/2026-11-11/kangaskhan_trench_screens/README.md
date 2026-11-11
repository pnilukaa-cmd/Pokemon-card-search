# Mega Kangaskhan ex / Legendary Trench wall, 2026-11-11

The ask: review a submitted Mega Kangaskhan ex / Bouffalant list built on
Delta Reign's healing (Legendary Trench, Tasty Rice Ball), Legendary
Pyroduct and a Team Rocket Petrel / Transceiver search engine. Write-up:
`decks/kangaskhan_legendary_trench_wall.md`.

All against the field in `decks/field` (107 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup; `kgc` is the 1000-game confirmation.

**Tags:**
- `kg1`: the submitted list (`K0`) and the field's Kangaskhan / Bouffalant
  wall (`F_cousin`).
- `kg2`–`kg6`: rounds 1–5. `kg4` has `F_cousin` again, paired with `M`.
- `kgc`: `O` (the final list), `K0` and `F_cousin`, 1000 games.

**Rounds** (`lists/`):
- `K0` (submitted), `k_*`.
- `L` (14 Energy, 4 Lillie's), `l_*`.
- `M` (Trench 2, Switch 2), `m_*`.
- `N` (Team Rocket engine 4), `n_*`.
- `O` (no Team Rocket engine: the final list), `o_*`.

**Measurements** (`measure/`): `measure_wall.py`, 10 logged games against
each of the eight decks in `../../2026-11-06/malamar_screens/measure/opps8.txt`:
every heal Item with the damage before and healed and the Stadium in play,
every attack, Prizes by Pokémon Knocked Out, how games end
(`measure_K0.txt`, `measure_O.txt`). `baseline_*.txt`:
`simulate_baseline.py`, 1000 trials.

**Scripts:** `run_list_wt.sh`, `paired.py`, `wait_fr.sh`, `measure_wall.py`;
`variant.py` is in `../../2026-10-23/snorlax_screens`. Paths point at the
session scratchpad.
