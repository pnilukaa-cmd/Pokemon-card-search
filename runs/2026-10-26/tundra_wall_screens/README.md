# Tundra Wall screens, 2026-10-26

A build on request: a deck "focused on tankiness, damage reduction /
mitigation". Write-up: `decks/aurorus_kangaskhan_tundra_wall.md`.

All against the 97-deck field (before this deck joined it), tag `tk0`,
paired on the same seeds. Screens are 200 games per opponent; the
confirmation is 1000.

**Engine.** f117148 (damage walls keep their conditions; Basic Energy is
not Special), then 95007af (self_mill_cost on). The mill cost changes only
lists with Mega Abomasnow ex. Rounds 1-2 and their bases ran without it;
`*__self_mill_cost_*` are the knob runs; the round-4 Abomasnow re-tests
and both confirmations ran with it.

**Rounds** (each paired against the best list of the round before):
- `w1_` from `W0`. Best: `w1_kang`.
- `w2_` from `w1_kang`. Best: `w2_abom0` / `w2_cet0`.
- `w3_` from `w3_base`, both Stage 1 lines out. Best: `w3_e25`.
- `w4_` from `w3_e25`. Best: `w4_e27`.
- `w5_`, `w6_` from `w4_e27`. Final: `w6_padboss`.
- **Confirmation:** 1000 games for `W0` and `w6_padboss`.

**Scripts:**
- `variant.py BASE OUT 'Card SET NUM:+n' ...` writes a variant that stays at 60.
- `deckout.py LIST GAMES` counts how often the deck decks itself out. It
  found Hammer-lanche.
- `mitigation.py` and `energy_curve.py` (repo root) gave the mitigation
  and Energy numbers.
