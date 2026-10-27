# Mega Chandelure ex review screens, 2026-10-27

A submitted list (`user_raw.txt`; imported as `lists/X_user.txt` with the
pool's printings of Switch, Rare Candy and Basic Psychic Energy): Mega
Chandelure ex with Mew ex, Trevenant / Uxie, Elgyem, Unown and Patrat on
10 Energy. Write-up: `decks/mega_chandelure_ex_telepathic_hilda.md`.

All against the 98-deck field, paired on the same seeds, tag `ch1`
(engine aa450cf: "discard another card" is a cost). Screens are 200 games
per opponent; the confirmations are 1000.

**Rounds** (each paired against the best list of the round before):
- `c1_` from `X_user`. Best: `c1_line`.
- `c2_` from `c1_line`. Best: `c2_mix`.
- `c3_` from `c2_mix`. Best: `c3_notrevH` (no Trevenant line).
- `c4_` from `c3_notrevH`. Best: `c4_mew0h` (no Mew ex).
- `c5_` from `c4_mew0h`. Best: `c5_hilda4`, the final list.
- `c6_` from `c5_hilda4`. Nothing kept.
- `c7_` from `c5_hilda4`: Marshadow and Ariados. `c7_marsh1` screened
  +0.92 and confirmed at only +0.30 ± 0.25; not kept.
- **Lookahead check** (`*_la_ch1_50.json`, PILOT=lookahead, 50 games):
  `c3_notrevH` (2 Mew ex) against `c4_mew0h` (none): +2.51 ± 0.82 without
  Mew.
- **Confirmation** (`results/chc*.txt`): 1000 games for `X_user`,
  `c5_hilda4` and `c7_marsh1`.

`mega_chandelure_ex_retreat_tax_ch1_200.json` is the field's other Mega
Chandelure ex list on the same seeds.

**Measurements** (`measure/`):
- `ec_*.txt`: `energy_curve.py`, 10 games per opponent.
- `tally_*.txt`: `tally.py`, every action line per game over 60 logged
  games against six strong decks.

**Scripts:** `variant.py` (see `../../2026-10-23/snorlax_screens`),
`run_list.sh`, `paired.py`, `spread.py`, `tally.py`. Paths in
`run_list.sh` point at the session scratchpad.
