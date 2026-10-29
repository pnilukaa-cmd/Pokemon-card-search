# Kingdra ex review, 2026-10-28

A submitted list (`user_raw.txt`; imported as `lists/K_user.txt` with the
pool's printings: Kingdra ex SFA 12, Buddy-Buddy Poffin MEG 167, Night
Stretcher MEG 173, Prism Tower CRI 111, Poké Pad ASC 198, Gwynn PBL 109),
and the question whether a spread-damage mix adds anything. Write-up:
`decks/kingdra_ex_kings_order.md`.

All against the field in `decks/field`, paired on the same seeds within a
tag (`paired.py A B` prints B − A). Screens are 200 games a matchup.

**Tags:**
- `kg1`: the King's Order fixes with `recover_price` / `recover_fuel` as
  knobs (off; `_p_` price on; `_pf_` both), on `K_user` and the three
  Duskull decks. 200 games.
- `kg2`: the same three arms on `K_user` at 1000 games.
- `kg3`: e84da63, both knobs on. Every round below.
- `kgc`: the confirmation, 1000 games, `K_user` and the final list
  (`decks/field/kingdra_ex_kings_order.txt`, the same as `lists/B4.txt`).

**Rounds** (`lists/`):
- `k1_*` and `s_*` from `K_user`: tuning, and spread Pokémon for Energy
  Coin.
- `B2` = `K_user` without the Blaziken ex line, Energy Coin and Team
  Rocket's Factory. `r2_*` from `B2`, the spread ones like for like in the
  King's Order slots.
- `B3` = `B2` with a 4th Kingdra ex. `r3_*` from `B3`; `_la_` runs are the
  lookahead pilot at 50 games.
- `B4` = `B3` with one Ludicolo for a Water: the final list.

**Measurements:** `tally.py` (every action line of the deck's own, 60
logged games against six strong decks) and `inplay.py` (share of turns from
turn 3 with each Pokémon in play, and King's Order uses that passed up a
Hydro Pump Knock Out). Outputs are quoted in the write-up.

**Scripts:** `run_list_wt.sh`, `paired.py`, `tally.py`, `inplay.py`;
`variant.py` is in `../../2026-10-23/snorlax_screens`. Paths point at the
session scratchpad.
