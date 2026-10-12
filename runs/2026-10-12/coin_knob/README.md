# coin_expectation knob, 2026-10-12

While the pilot chose an attack, a coin-flip attack was priced by one real
flip on the game's random stream: Mega Kangaskhan ex's Rapid-Fire Combo
priced 500 on one call and 200 on the next. The knob priced it as the
average of 24 flips on a private stream instead.

Measured paired (tag ce1, 200 games against each of the 86 field decks).
`__c0` is knob off. `__c1` is knob on for the measured deck only
(`PILOT=probe PROBE_KNOBS=coin_expectation=1`), so the field plays the same.

| Deck | Paired (on − off) |
|---|---|
| Chandelure / Maushold wall | −0.04 ± 0.43 |
| Hop's Snorlax stacked buff | +0.01 ± 0.01 |
| Kangaskhan / Tyrantrum flip mill | −0.33 ± 0.56 |
| Maushold Gnaw Together mill | +0.03 ± 0.42 |
| Raging Bolt | −0.38 ± 0.49 |
| Slowking | −0.13 ± 0.53 |
| Team Rocket's Honchkrow / Kangaskhan | −0.20 ± 0.45 |
| Team Rocket's Hypno / Exeggutor | +0.26 ± 0.41 |
| Team Rocket's Raticate / Ampharos | −0.45 ± 0.51 |
| Team Rocket's Raticate rush | +1.02 ± 0.49 |

Mean −0.02. Removed (engine commit after this one).
