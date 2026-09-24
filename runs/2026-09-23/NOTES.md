## What changed since the 45-deck table

**The field.** 54 decks, up from 45. Added: `wugtrio_paralysis_pin`,
`tauros_risky_ruins`, both Cradily condition builds, and the five mill
study lists. Removed: `selective_bloom_cradily` (no Basic Pokémon, cannot
start a game) and `paralysis_ctl` (a measurement control, not a deck).
30th Celebration (`30C`) is treated as legal; two Maushold lists use it.

**The engine.** Four commits landed after the 45-deck table: the
copy-attack depth guard, the three loose searches (Cyrano, the Ascension
family, Crispin's "different types"), Binding Mochi and Hop's Choice Band
in `DAMAGE_TOOLS`, and Repel / Iron Defender / the when-damaged Tools.

**Same seeds.** Every pairing reuses the `rr1` seed of the previous run,
so a deck present in both runs faces the same dice against the same
opponent.

## How far the old decks moved

Dropping `selective_bloom_cradily` removes a near-certain win from every
deck, which lowers a mean of *m* by about (99.7 − *m*) / 43: −0.6 at the
top of the table, −2.0 at the bottom. After removing that, and scoring
only against the opponents both runs share, the residual moves have a
standard deviation of 0.77. Three decks stand out:

| deck | residual | cause |
|---|---:|---|
| `water_aggro` | −3.51 | **Crispin fix, measured.** Paired A/B across commit `3ec19f3`, `water_aggro` vs all 53 opponents at 400 games: **−4.18 ± 0.50**. The deck is mono-Water with 4 Crispin; Crispin had been fetching 2 Energy where the printed "of different types" allows 1. Neither of the commit's other two fixes is in its list. |
| `hops_snorlax_stacked_buff` | +2.07 | Consistent with Hop's Choice Band now applying its damage. Not isolated by A/B. |
| `meta_slowking` | −1.85 | Consistent with the copy-attack depth guard and Lucky Helmet. Not isolated by A/B. |

No other deck moved by more than 1.4 after the correction.
