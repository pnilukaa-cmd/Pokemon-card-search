# Mega Malamar ex deck, 2026-11-06

The ask: a Darkness deck around Inkay and Mega Malamar ex (Delta Reign),
with Sableye to disrupt the hand and maybe Toxtricity for Energy. Write-up:
`decks/mega_malamar_ex_psychic_marionette.md`.

The English Delta Reign set isn't in api.pokemontcg.io or TCGdex yet.
`tcgdex_m6/` holds the Japanese Storm Emeralda data the three provisional
cards (Sableye DLR 60, Inkay DLR 68, Mega Malamar ex DLR 69) were built
from: the set list and cards M6-046, M6-047, M6-048, fetched from
api.tcgdex.net on 2026-11-06.

All against the field in `decks/field` (104 decks), paired on the same
seeds within a tag (`paired.py A B` prints B − A). Screens are 200 games a
matchup.

**Tags:**
- `mm1`: b2d5545's engine before it was committed, with the
  `bench_fill_payoff` knob (`M0_bf`; taken out).
- `mm2`, `mm3`, `mm4`: b2d5545.
- `mmc`: the confirmation, 1000 games: `M0` and the final list (`M2d`).

**Rounds** (`lists/`):
- `M0`: the list as asked. `m_*` from it.
- `M1` = `m_mb0` (no Mandibuzz line, a 4th Mega Malamar ex). `n_*` from it.
- `M2a`–`M2d` combine round 2; the final list is `M2d`. `p_*` from it.

**Measurements** (`measure/`, 10 logged games against each of the eight
decks in `opps8.txt`): `attacks_bench.py`, every attack with the
opponent's Bench at the attack and the Prizes it took
(`attacks_final.txt`); `baseline_*.txt`, `simulate_baseline.py`, 1000
trials.

**Scripts:** `run_list_wt.sh`, `paired.py`, `attacks_bench.py`, `tally.py`;
`variant.py` is in `../../2026-10-23/snorlax_screens`. Paths point at the
session scratchpad.
