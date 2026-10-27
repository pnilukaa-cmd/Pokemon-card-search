# Tundra Wall revision screens, 2026-10-27

The question: mix the Snorlax / Bouffalant / Kangaskhan deck's strategy
(Snorlax, Good Sleep, its mitigation) into the Aurorus / Mega Kangaskhan
ex Tundra Wall deck, add heals and disruption, and cut its 27 Energy.
Write-up: `decks/aurorus_kangaskhan_tundra_wall.md`.

All against the 98-deck field, paired on the same seeds within a tag.
Screens are 200 games per opponent; the confirmation is 1000.

**Tags:**
- `tk1`: 927c086.
- `tk2`: 2ee4fb9. Fossils are Items outside play.

**Rounds** (each paired against the best list of the round before):
- `m1_` from `T0` (the 2026-10-26 list, 27 Energy), tk1. Best: `m1_mix`.
- `m3_` from `m1_mix`, tk2. `T0` and `m1_mix` re-run on tk2 as the
  baselines. Best: `m3_ham4`, the final list.
- `m4_` from `m3_ham4`, tk2. Nothing kept.
- `x1_` from `X0` (the Snorlax / Bouffalant / Kangaskhan field list), tk2:
  heals, disruption, and this deck's wall moved into it (`x1_tundra*`).
- `x2_` from `x1_icee`, tk2: more Jumbo Ice Cream.
- **Confirmation:** 1000 games on tk2 for `T0` and `m3_ham4`
  (`results/c1000.txt`); and for `X0` and `x2_icekofu`
  (`results/c1000x.txt`).

**Field note.** The field's copy of the Tundra Wall deck was `T0` for
every run here except `X0` at 1000 games. During `x2_icekofu` at 1000 it
was swapped for `m3_ham4`, so that one matchup is left out of the X0 /
x2_icekofu pairing.

**Measurements** (`measure/`, with `m3_ham4` as the field's copy):
- `mitigation.txt`: `mitigation.py`, 5 games per opponent. It now also
  reports HP healed and the opponent's Energy removed per game.
- `goodsleep.txt`: `goodsleep.py`, Snorlax attacks, Good Sleep heals and
  Snorlax Knock Outs per game, 2 games per opponent.
- `ec_*.txt`: `energy_curve.py`, 10 games per opponent (with `T0` as the
  field's copy).

**Scripts:**
- `variant.py BASE OUT 'Card SET NUM:+n' ...` writes a variant that stays at 60.
- `run_list.sh TAG GAMES SUMMARY deck.txt...` runs each list against the
  field (`vs_field.py`, 4 jobs). Its paths point at the session scratchpad.
- `paired.py A.json B.json` prints B − A over the common opponents.
- `spread.py A.json [B.json]` prints the mean, median, worst, best and
  meta matchups, with B's figures beside them.
- `goodsleep.py LIST GAMES` (see above).

The `heal_saves_ko` pilot check is in `../pilot_checks`.
