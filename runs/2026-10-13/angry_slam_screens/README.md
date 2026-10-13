# Aggron Angry Slam / Diggersby screens, 2026-10-13

Question: "a deck with Aggron's Angry Slam, where you spread some damage on
your own Bench with Diggersby?"

All runs are against the 89-deck field, paired on the same seeds within a
tag. Screens are 200 games per opponent; the confirmation is 1000.

**Start lists (tag ag0, then rerun on ag1):**
- `A_dig_ruins`: Aggron + Diggersby + 3 Risky Ruins.
- `B_ruins_emolga`: no Diggersby; Risky Ruins, Emolga's Sky Wave and Venture
  Bomb arm Angry Slam.
- `C_dig_noruins`: A with Venture Bomb in place of Risky Ruins.
- `E_dig_ruins_bomb`: A with Venture Bomb in place of Poké Pad.
- `R_dig_munk`: the existing `diggersby_munkidori_earthquake` field list,
  for reference.

**Pilot knobs (tag ag0, `K_`):** list A with the probe pilot.
- `K_feed60`, `K_feed100`: feed_bench_hitter, not kept.
- `K_ko60`, `K_ko120`, `K_ko240`, `K_ko1`, `K_both`: self_bench_ko_cost.
  The value was absolute in the first runs and a multiple of
  ko_bonus_per_prize in `K_ko1` / `K_munk_ko1`.

`self_bench_ko_cost` went on by default (commit 07123e3). That changes how
the field's Diggersby deck plays, so everything after was rerun on tag ag1.

**Tuning:**
- **Aggron:** rounds `r1_`, `r2_`, `r3_` from A. The final list is
  `r2_noballoon`.
- **Gourgeist ex:** `X_gourgeist` is the Aggron list with Gourgeist ex as
  the payoff. Rounds `g1_` and `g2_` follow; the final list is `g2_sb`.
- **Confirmation:** 1000 games for `r2_noballoon`, `g2_sb`, `A_dig_ruins`,
  `R_dig_munk` and `X_gourgeist`.

`variant.py BASE OUT 'Card SET NUM:+1' ...` writes a variant that stays at
60 cards.

**Write-ups:**
- `decks/aggron_diggersby_angry_slam.md`
- `decks/gourgeist_diggersby_horrifying_rondo.md`
