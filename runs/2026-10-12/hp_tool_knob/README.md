# hp_tool_to_attacker knob, 2026-10-12

Hero's Cape went onto whatever was Active. In a Cinderace deck that is the
Cinderace pivot, and Core Memory took the Zygarde's Tool slot first. The
knob put an HP Tool on the Pokemon with the best castable attack (then the
most Energy), attaching HP Tools before other Tools.

Measured paired, tag hp1: 200 games against each of the 86 field decks.
`__h0` is knob off; `__h1` is knob on for the measured deck only
(`PILOT=probe PROBE_KNOBS=hp_tool_to_attacker=1`).

| Deck | on − off |
|---|---|
| Diggersby / Munkidori | −0.13 ± 0.46 |
| Ditto Hydreigon | −0.05 ± 0.45 |
| Golbat / Brute Bonnet | −0.35 ± 0.50 |
| Heracross / Sinistcha | +1.95 ± 0.48 |
| Kyurem / Vanilluxe | +0.43 ± 0.44 |
| Mega Zygarde ex / Cinderace | +0.28 ± 0.40 |
| Mega Excadrill | +0.37 ± 0.52 |
| Mew / Pikachu box | −0.61 ± 0.28 |
| Scovillain / Salazzle | +0.01 ± 0.54 |
| Team Rocket's Tyranitar | +0.10 ± 0.46 |

Mean +0.20, mixed. Removed.
