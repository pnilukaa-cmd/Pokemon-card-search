# Gothitelle hand-cut deck, 2026-11-02

The ask: a deck around Gothitelle's Distorted Future (the opponent's hand
to 3), with an easy hand discard (Talonflame's Sky Hunt), Rare Candy, and
Fletchling's Chirp to find the Pokémon with Fighting Resistance. Write-up:
`decks/gothitelle_noivern_distorted_future.md`.

All against the field in `decks/field` (103 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup.

**Tags:**
- `go1`: `V0`, the list as asked, greedy (`_g_`) and with `hand_match`
  (`_hm_`; then a knob, off by default). The first `_hm_` runs crashed
  (Ultra Ball pitching the next Ultra Ball) and were re-run after the fix.
  `nv2_hm` here is void: Tuning Echo was not yet gated, and Noivern
  attacked for free on any hand.
- `go2`: the Tuning Echo gate in; all `_hm_`. `kk` here still had Chirp
  finding any Pokémon.
- `go3`: Chirp's Resistance filter in; all `_hm_`.
- `go4` to `go7`: bfb7a80 (`hand_match` on by default), all `_g_`.
- `goc`: the confirmation, 1000 games: `V0` and the final list (`i_ch2`).

**Rounds** (`lists/`):
- From `V0`: `ib2` (Iron Boulder), `nv2` (Noivern 2-2), `ht2` (Hand
  Trimmer), `kk` (Krookodile 2-1-2), `li2` (2 fewer Lillie's), `tf3` (a
  3rd Talonflame line), `xe0`/`xe4` (Xerosic's), `nv2ib`, `tf0` (no
  Talonflame line), `e12` (12 Energy), `nvtf0` (Noivern, no Talonflame).
- `F1`–`F5` combine them; `F4` (Noivern, no Talonflame, 14 Energy) won.
- `k_*` from `F4`; `H` = `k_nb4` (4 Noibat for 2 Fletchling).
- `h_*` from `H`; `I` = `h_fl0` (no Fletchling).
- `i_*` from `I`; the final list is `i_ch2` (2 Team Rocket's Chingling).

**Measurements** (`measure/`, 10 logged games against each of the eight
decks in `opps8.txt`): `attacks.py`, every attack with both hand sizes at
the attack, whether they matched, and the Prizes it took
(`attacks_first_list.txt` is `V0` on bfb7a80); `baseline_*.txt`,
`simulate_baseline.py`, 1000 trials.

**Scripts:** `run_list_wt.sh`, `paired.py`, `attacks.py`; `variant.py` is
in `../../2026-10-23/snorlax_screens`. Paths point at the session
scratchpad.
