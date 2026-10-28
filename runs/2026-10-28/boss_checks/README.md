# Boss's Orders checks, 2026-10-28

The question: Boss's Orders is a mainstay in almost every meta deck, so why
did it measure worse than an Energy in the Jellicent ex and Mega Chandelure
ex lists? Write-ups: `decks/jellicent_ex_oceanic_curse.md` (*Boss's Orders,
re-measured*) and `decks/mega_chandelure_ex_telepathic_hilda.md`.

All runs are against the field in `decks/field` (100 decks), 200 games a
matchup, paired on the same seeds within a tag (`paired.py A B` prints
B − A).

**Tags:**
- `gk1`: 243a582's gust rule under PILOT=probe (`_k_`) against greedy
  (`_g_`), before it was committed.
- `gk2`: 243a582, Boss's Orders played for a Knock Out (`gust_for_ko`).
  Variants: `_s1_`/`_s2_` the strand rule only under an Item lock / always
  (knob `gust_strand` 1 / 2 then); `_f1_` Boss's Orders ahead of Hilda and
  the draw Supporters; `_fl_` that and a second look before the attack.
  The last two were removed.
- `gk3`: 27be9e3, the strand rule on. `meta_dragapult_dusknoir_g` and
  `dd_b0_g` are from 9d7eb51: the 27be9e3 run of the first crashed (a gust
  with no Active to switch with). 9d7eb51 plays the same as 27be9e3 in
  every game that never reaches that state. The 27be9e3 `dd_b0` is kept as
  `dd_b0_g_gk3_200_27be9e3.json`. `_v_`: when the Active is as good a
  Knock Out, gust the Benched Pokémon with more invested in it
  (`gust_value`, never committed).

**Lists** (`lists/`):
- `jb0`–`jb4`: the Jellicent ex list with 0–4 Boss's Orders, Basic
  Psychic Energy making up the rest. `jb1` is the published list.
- `jbh`, `jbf`: `jb1` with a 2nd Boss's Orders for a Crushing Hammer / a
  Handheld Fan.
- `cb1`–`cb4`: the Mega Chandelure ex list with 1–4. `cb3` is the
  published list.
- `cbn`, `cbu`: `cb3` with a 3rd Night Stretcher / a 4th Ultra Ball for a
  Boss's Orders.
- `dp_b0`, `nz_b0`, `rb_b0`, `dd_b0`: Dragapult ex, N's Zoroark ex, Raging
  Bolt ex and Dragapult ex / Dusknoir with their 3 Boss's Orders replaced
  by 3 Basic Energy of their types.
- `dp_h0`: Dragapult ex with 3 of its 4 Crushing Hammer replaced by Energy.
- `nz_t0`: N's Zoroark ex with its 2 Binding Mochi and Venture Bomb replaced
  by Energy.

**Measurements** (`measure/`):
- `gust_audit.txt`: `gust_audit.py`, why Boss's Orders sat in hand.
- `energy.txt`: `energy_curve.py` for Dragapult ex with and without its
  Boss's Orders, and `energy_where.py`, where its 8 Energy are each turn.
- `gust_counts.txt`: `gusts_wt.py`, Boss's Orders played a game and the
  share Knocked Out that turn, under the rules tried.

**Scripts:** `run_list_wt.sh` (a list of decks from a given tree, pilot
and tag), `paired.py`, `energy_where.py`, `gusts_wt.py`. Paths point at the
session scratchpad.
