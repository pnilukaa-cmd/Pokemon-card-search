# Bug Out (Masquerain / Jellicent), 2026-11-09

The ask: check whether the Delta Reign cards are in the card APIs now, with
a submitted Bug Out list. They are (pokemontcg.io, set me6, code DLR);
merged with `fetch_pokemon_cards.py --merge-set me6`. Write-up:
`decks/bug_out_masquerain_jellicent.md`.

All against the field in `decks/field` (105 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup; `boc` is the 1000-game confirmation.

**Tags:**
- `bo1`: the submitted list with `STACK_BOTTOM` on (`B0`) and off (`B0_sb0`).
- `bo2`: `HOLD_BOTTOM_FUEL` on (`B0_hb1`) and off (`B0_hb0`).
- `bo3`–`bo8`: list rounds 1–6.
- `boc`: the confirmation, `X` (the final list) and `B0`, 1000 games.
- `cz`: the three Centiskorch field decks (Sizzlipede PBL 9 has Bug Out)
  on f342763's engine (`old_*`, run in a worktree of it) and the new one
  (`new_*`).

**Rounds** (`lists/`): `B0` submitted, `b_*` from it; `T` (all Grass),
`t_*`; `U`, `u_*`; `V`, `v_*`; `W`, `w_*`; `X` (final), `x_*`.

**Measurements** (`measure/`): `measure.py`, 10 logged games against each
of the eight decks in `../../2026-11-06/malamar_screens/measure/opps8.txt`:
every attack, and for Bug Out where its Bug Out Pokémon were
(`measure_X.txt`, `measure_B0_final.txt`; `measure_B0_before_holdback.txt`
is the submitted list before `hold_bottom_fuel`). `baseline_*.txt`,
`simulate_baseline.py`, 1000 trials.

**Scripts:** `run_list_wt.sh`, `paired.py`, `wait_fr.sh`, `measure.py`;
`variant.py` is in `../../2026-10-23/snorlax_screens`. Paths point at the
session scratchpad.
