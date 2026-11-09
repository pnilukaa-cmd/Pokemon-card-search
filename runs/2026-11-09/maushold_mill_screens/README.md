# Maushold mill (Legendary Summit, Tauros), 2026-11-09

The ask: study a submitted Maushold mill list as a mill deck, then review
the newest cards for new mill combinations. Write-up:
`decks/maushold_mill_legendary_summit.md`.

All against the field in `decks/field` (106 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup; `mlc` is the 1000-game confirmation.

**Tags:**
- `ml1`: the submitted list (`M0`) after dabfb36's fixes.
- `ml2`–`ml5`: rounds 1–4.
- `mlc`: the final list (`Q`), the submitted list (`M0`) and the field's
  existing Maushold mill deck (`R_field_maushold`), 1000 games.

**Rounds** (`lists/`):
- `M0` (submitted), `m_*`: the Delta Reign candidates, each in the
  Pokémon Catcher slots.
- `N` (+2 Tauros), `n_*`: the published-list pieces.
- `P` (4 Tauros, 1-1 Dunsparce), `p_*`.
- `Q` (no Dunsparce line, the final list), `q_*`.

**Measurements** (`measure/`): `measure_mill.py`, 10 logged games against
each of the eight decks in `../../2026-11-06/malamar_screens/measure/opps8.txt`:
every attack with the cards it milled and the Maushold in play, how each
game ended, the Prizes on each side (`measure_M0.txt`, `measure_Q.txt`).
`baseline_*.txt`: `simulate_baseline.py`, 1000 trials.

**Scripts:** `run_list_wt.sh`, `paired.py`, `wait_fr.sh`,
`measure_mill.py`; `variant.py` is in `../../2026-10-23/snorlax_screens`.
Paths point at the session scratchpad.
