# Delta Reign cards for mill and hand disruption, 2026-11-10

The ask: which Delta Reign cards improve the mill / hand-disruption
archetype. Every Delta Reign card was read (set `me6`, not by name: the
Delta Reign Rotom, Sharpedo and Liepard have no hand disruption; Astonish,
Chew Off and Knock Off are on older printings of those names).

The ones that could fit, each added to a field deck that can pay for it,
paired against that deck unchanged on the same seeds (tag `ml6`, 200 games
a matchup, 107-deck field; `paired.py A B` prints B − A):

| Change | Host | Measured |
|---|---|---|
| +2 Mantine (Make Waves), −Catcher −Aarune | `Q` = maushold_mill_legendary_summit | −3.53 ± 0.55 |
| +1-1 Surskit / Masquerain (Frightening Pattern), −Catcher −Aarune | `Q` | −1.83 ± 0.47 |
| +2 Giratina (Chaos Crawler), −Catcher −Aarune | `Q` | −3.70 ± 0.53 |
| +2 Inkay (Knock Off), −Energy Search −Air Balloon | `KR` = krookodile_ex_relicanth_hand_disruption | −2.77 ± 0.49 |
| +2 Inkay (Knock Off), −2 Basic Darkness Energy | `AB` = mega_absol_ex_hand_lock | −5.31 ± 0.49 |
| +1-1 Sandshrew / Sandslash (Digging Claw), −2 Air Balloon | `KT` = kangaskhan_tyrantrum_flip_mill | −1.00 ± 0.44 |

Make Waves was checked for pilot misuse: 14 uses in 40 games against the
eight decks in `../../2026-11-06/malamar_screens/measure/opps8.txt`, into
an average opposing hand of 3.4, taking 0.6 cards a use off their deck.

Measured earlier (`../2026-11-09/maushold_mill_screens`): Legendary Summit
(−12.65 to take out of a Maushold mill list) and Tauros (+3.09, +2.30,
+2.96) are the Delta Reign cards that help; Grisham, Tasty Rice Ball,
Custom Vest, Swablu / Altaria, Legendary Pyroduct and Eevee lost 2–4.

## Supporters (tag `ml7`, `lists_supporters/`)

The newest sets' Supporters that touch the opponent's hand or deck, or
draw, swapped into the same Maushold mill list (`Q`), paired against it:

| Change | Measured |
|---|---|
| +2 Tate & Liza's Training (DLR), −Aarune −Pokégear 3.0 | −2.34 ± 0.55 |
| +2 Eri, −Lana's Aid −Night Stretcher | −2.84 ± 0.46 |
| +2 Emma (CRI) for 2 Lillie's Determination | −5.53 ± 0.57 |
| +2 Tate & Liza's Training for 2 Lillie's | −5.58 ± 0.55 |
| Xerosic's Machinations 2 → 4 for 2 Lillie's | −5.62 ± 0.69 |
| +2 Emcee's Hype (DLR reprint) for 2 Lillie's | −6.34 ± 0.63 |
| +2 Judge (POR reprint) for 2 Lillie's | −6.36 ± 0.56 |
| +2 Lucian for 2 Lillie's | −7.64 ± 0.62 |

Tate & Liza's Training goes back to the hand while a "Legendary" Stadium is
in play (Legendary Summit is one); that return was not modeled before this
run. The pilot plays Lillie's on a hand of 4 or fewer and Tate & Liza's on
bigger ones. `measure/measure_s_tlb.txt` (80 games) shows no change in how
games end (52 wins, 4 own deck-outs; the list without it: 53, 5): the
-2.34 is too small for 80 games to explain.
