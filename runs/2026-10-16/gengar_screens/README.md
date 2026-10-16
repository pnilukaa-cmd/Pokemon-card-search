# Mega Gengar ex / Gengar ex screens, 2026-10-16

A submitted list (`user_raw.txt` as pasted, with the Energy line cut off at
"10 Da", read as 10 Basic Darkness Energy; imported as `lists/G_user.txt`).
No question came with it, so it was reviewed like the earlier submitted
lists: validate, check the engine, measure, tune, confirm.

All runs are against the 93-deck field, paired on the same seeds within a
tag. Screens are 200 games per opponent; the confirmation is 1000.

**Tags.** Each engine fix that changed a field deck got a new tag, and the
base of the next round was re-run on it.
- `gg0`: engine 0e9e575 (Chaotic Pain and Void Gale fixed).
- `gg1`: + prize modifiers on the side they name, and counter attacks
  ranked by their counters (37a3692).
- `gg2`: + Sinister Surge / Glass Trumpet Energy to the neediest (6558f6e).
- `gg3`: + look-and-attach cards and "to 1 of your X Pokémon" (03e17d5).

**Rounds** (each paired against the best list of the round before):
- `g1_`: from `G_user` (gg0, re-run on gg1). Best: `g1_nido0e`.
- `g2_`: from `g1_nido0e`, on gg1 and again on gg2 after the Sinister
  Surge fix (`res_g2_gg1.txt`, `res_g3.txt`). Best: `g2_e2munk`.
- `g4_`: from `g3_base` (= `g2_e2munk`) on gg3. Nothing beat it.
- `g5_`: from `g3_base` on gg3. Best: `g5_dawn3cape`, the final list.
- `g6_`: Energy Trainers screened against the final list on gg3.
- **Confirmation:** 1000 games on gg3 for `G_user`, `g3_base`,
  `g4_nido` (the Nidorina engine put back) and `g5_dawn3cape`.

**Pilot checks** (`lists/pilot_checks`, results under the same names):
- `K_cp0`, `K_nido_cp0`: counter_potential off (gg1).
- `K_<field deck>` with `PROBE_KNOBS=counter_potential=0` (gg1): the field
  decks whose attacks place counters.
- `K_G_user` and `K_<field deck>` with `evolve_pick=1` (gg1): Grand Tree,
  Dark Awakening and Ascension decks. Noise everywhere; left off.
- `EA_*` with `each_attach_rank=1` (gg1). Kept on.

**Scripts:**
- `variant.py BASE OUT 'Card SET NUM:+n' ...` writes a variant that stays
  at 60 cards, and reads each card's section from the card file.
- `round.sh BASE PREFIX` writes the round-2 variants.
- `boardgame.py LIST OPP SEED` plays one verbose game and prints your board
  (Energy, damage, hand) at the end of each of your turns. It found the
  Sinister Surge spreading.

Write-up: `decks/mega_gengar_ex_toxtricity_chains.md`.
