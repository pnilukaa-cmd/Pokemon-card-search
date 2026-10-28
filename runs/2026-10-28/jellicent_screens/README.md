# Jellicent ex review and Chandelure mixes, 2026-10-28

A submitted list (`user_raw.txt`; imported as `lists/J_user.txt` with
Pokégear 3.0 BLK 84 and Basic Psychic Energy), and the question whether
it can be mixed with the Mega Chandelure ex list (`lists/C0.txt`, the
2026-10-27 final). Write-up: `decks/jellicent_ex_oceanic_curse.md`.

All against the 99-deck field, paired on the same seeds within a tag.
Screens are 200 games per opponent; the confirmation is 1000.

**Tags:**
- `je2`: 4bdff48. Ignition Energy is discarded at end of turn; Stage
  Energy follows its holder. (A first round on `je1`, the engine before
  that fix, was stopped and rerun here.)
- `je3`: 94c272f. Ignition goes only where it is spent that turn.

**Rounds:**
- `j_` from `J_user` and `m_` from `C0` (je2): tuning, and the mixes.
- `te` (je2): `J_user` under PILOT=probe with temp_energy_now=1.
- `j3_` from `j_ign0` (je2). Best: `j3_boss3`.
- `j4_` from `j4_base` = `j3_boss3` (je3). Best: `j4_boss2`.
- `j5_` from `j4_boss2` (je3). Best: `j5_boss1`, the final list.
- `j6_` from `j5_boss1` (je3). Nothing kept.
- **Confirmation** (`results/jec.txt`): 1000 games on je3 for `J_user`
  and `j5_boss1`.

**Measurements** (`measure/`): `ec_*` (`energy_curve.py`, 10 games per
opponent) and `tally_*` (`tally.py`, 60 logged games against six strong
decks; `tally_m_fr2j2` is the Chandelure list with 2 Frillish and 2
Jellicent ex).

**Scripts:** `run_list.sh`, `run_list_wt.sh` (same, from another tree and
pilot), `paired.py`, `spread.py`, `tally.py`; `variant.py` is in
`../../2026-10-23/snorlax_screens`. Paths point at the session scratchpad.
