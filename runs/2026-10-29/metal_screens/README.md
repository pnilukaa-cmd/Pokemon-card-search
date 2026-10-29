# Orthworm ex / Metang review, 2026-10-29

A submitted list (`user_raw.txt`; imported as `lists/M_user.txt` with the
pool's printings and Boss's Orders MEG 114 for the rotated LOR-TG 24), and
the question which strong Metal Pokémon to add. Write-up:
`decks/orthworm_ex_metang_archaludon.md`.

All against the field in `decks/field` (101 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A).

**Tags:**
- `mg1`: 5d7a3c1 with Brock's Scouting's Evolution half read
  (`brock_evolution` on; `_b0_` off). It measured worse and was removed;
  every list in a round shares it. 200 games.
- `mgc`: b6759de, 1000 games: `M_user` and the two finalists.

**Rounds** (`lists/`):
- `c_*`, `a_*`, `t_*` from `M_user`: Metal Pokémon and Trainers, paid for
  with the 2 Energy Recycler (and a Heavy Baton for a 3-card line).
- `M2` = `a_archex` (Archaludon ex + 2 Duraludon). `r2_*` from `M2`.
- `M3` = `M2` with 2 Genesect ex for the 2 Petrel and Metal Energy for
  Metagross. `r3_*` from `M3`.
- `F1` = `r3_arx2` (a 2nd Archaludon ex for the last Heavy Baton); `F2` =
  `F1` with 2 Metal Energy for 2 Jumbo Ice Cream: the final list.

`summary_m3.txt` is filtered from a scratch file an earlier session also
wrote to. **Scripts:** `run_list_wt.sh`, `paired.py`, `tally.py`; paths
point at the session scratchpad.
