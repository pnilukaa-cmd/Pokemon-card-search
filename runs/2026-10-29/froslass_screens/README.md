# Mega Froslass ex review, 2026-10-29

A submitted Mega Froslass ex / Chandelure / Dudunsparce list
(`user_raw.txt`; imported as `lists/F_user.txt` with the pool's printings
for Boss's Orders MEG 114, Rare Candy MEG 125, Energy Search POR 72, Ultra
Ball MEG 131 and Pokégear 3.0 BLK 84), and the question how it wins:
forcing draws for big Resentful Refrain hits, and any other win
conditions. Write-up: `decks/mega_froslass_ex_resentful_refrain.md`.

All against the field in `decks/field` (102 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup.

**Tags:**
- `fr1`: 743873b's engine before it was committed (Lucian as printed).
  `F_user_old` is the same list on 15fb3c8 (Lucian as "each player draws
  3"); `F_user_hr` has `heal_refuel` on.
- `fr2`: that and the Lucian bench rule (later taken out). `F_user_od1` /
  `_od2`: Alluring Light only on a turn a hand-counting attack fires /
  never (`opp_draw_gate`, taken out).
- `fr3`, `fr4`, `fr5`: 51ff3d5. `_hr_` runs have `heal_refuel` on.
- `frc`: the confirmation, 1000 games: `F_user`, the final list (`G4`), and
  `G4` with `heal_refuel` (taken out: +0.21 ± 0.22). The final list joined
  `decks/field` while this ran, so the two `G4` runs include the mirror
  (49.1%) and count 103 decks; the write-up's 71.02% leaves it out, and
  `paired.py` pairs only the opponents both runs played.

**Rounds** (`lists/`):
- Round 1 (`fr1`) from `F_user`: `l0`/`l1` (Lucian), `c2`/`c4`
  (Chandelure), `b0` (Budew), `w1` (Wally's), `hc0` (Hero's Cape), `bc0`
  (Battle Cage), `mf4` (4th Mega Froslass ex), `s0` (Salvatore), `p0`
  (Petrel). Each cut card is replaced by Ultra Ball.
- Round 2 (`fr2`): `w1n` (`w1` with Night Stretcher for the Ultra Ball);
  `G1` = `mf4`, and `g_*` from it, each for a Petrel.
- Round 3 (`fr3`): `G2` = `g_sn4` (4th Snorunt); `h_*` from it, cuts
  replaced by Night Stretcher.
- Round 4 (`fr4`): `G3` = `h_e7` (7th Energy); `i_*` from it.
- Round 5 (`fr5`): `G4` = `i_comb` (9 Energy, 4 Night Stretcher, no Ultra
  Ball or Lucian): the final list. `j_*` from it.

**Measurements** (`measure/`, 15 or 10 logged games against each of the
eight decks in `opps8.txt`):
- `attacks.py`: every attack, the opposing hand it hit, what the deck
  added to that hand that turn, and the Prizes it took
  (`attacks_submitted.txt` and `attacks_submitted_alluring_off.txt`, with
  `OPP_DRAW_GATE=2`, on fr2's engine; `attacks_final.txt` on 51ff3d5).
- `inplay.py`: share of turns from turn 3 with Mega Froslass ex / Snorunt
  / Chandelure in play, G1 against G2.
- `water.py`: turns an Active Mega Froslass ex ended without attacking and
  without Water, and where the Energy went, G2 against G4.
- `tally.py`: every action line of the submitted list.
- `baseline_*.txt`: `simulate_baseline.py`, 1000 trials.
- `known_leak.py`: Supporters with a hand-written rule that the card-text
  fallback still played, across the field (how the Lucian leak was found).

**Scripts:** `run_list_wt.sh`, `paired.py` and the measurement scripts
above; `variant.py` is in `../../2026-10-23/snorlax_screens`. Paths point
at the session scratchpad.
