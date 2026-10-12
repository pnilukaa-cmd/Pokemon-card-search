# Big Basic screens for the Cinderace / Mega Zygarde ex list, 2026-10-12

The question: which other big-HP, high-damage Basics work alongside
Cinderace's Turbo Flare?

The base list was `decks/field/mega_zygarde_cinderace_gaia_wave.txt` as of
2026-10-11 (`lists/bb_base.txt`). Each variant ran 200 games against each of
the 86 field decks, paired with the base on the same seeds (tag bb2). The
best were rerun at 1000 games (tag bbc), base included.

Engine:
- bb2 ran on 95ec605.
- The later runs ran on bdeff85, which only removes a knob that was off.

Before screening, each candidate's attack was checked on a fixed board
(cost payable, damage as printed).

## Swap: the candidate replaces Mega Audino ex (`bb_<card>.txt`)

Off-type attackers also trade Basic Fighting Energy for their own type,
usually three. Latias got 2 Fire + 2 Psychic, Zacian 4 Metal, and Pikachu ex
2 each of Grass, Lightning and Metal.

Costs: F Fighting, W Water, M Metal, P Psychic, D Darkness, C Colorless; mixed
and Fire costs are spelled out.

| Candidate | HP | Attack | Win % | Paired vs base (82.00%) |
|---|---|---|---|---|
| Cornerstone Mask Ogerpon ex TWM 112 | 210 | Demolish FCC 140, ignores effects | 81.93 | −0.07 ± 0.58 |
| Mega Hawlucha ex ASC 116 | 250 | Somersault Dive FFC 120 (+140 with a Stadium) | 80.80 | −1.20 ± 0.49 |
| Mega Kangaskhan ex MEG 104 | 300 | Rapid-Fire Combo CCC 200 + 50 per heads | 80.62 | −1.38 ± 0.47 |
| Regirock ex ASC 107 | 230 | Giant Rock FCCC 140 (280 vs Stage 2) | 79.42 | −2.58 ± 0.44 |
| Stunfisk ex ASC 114 | 210 | Flopping Trap FCC 100 (200 if damaged) | 79.26 | −2.74 ± 0.43 |
| Snorlax ex PRE 76 | 260 | Toss-and-Turn Press CCCC 120 per heads ×3 | 78.94 | −3.06 ± 0.47 |
| Koraidon ex TEF 120 (+3 Fire) | 230 | Kaiser Tackle (Fire + 2 Fighting) 280, 60 to itself | 78.52 | −3.48 ± 0.51 |
| Bloodmoon Ursaluna ex TWM 141 | 260 | Blood Moon CCCCC 240 | 78.30 | −3.70 ± 0.45 |
| Iron Boulder ex TEF 192 | 240 | Power Stomp FFC 200, discard 2 | 77.72 | −4.28 ± 0.51 |
| Gouging Fire ex TEF 188 (+3 Fire) | 230 | Blaze Blitz (2 Fire + C) 260 | 77.40 | −4.60 ± 0.46 |
| Black Kyurem ex SSP 218 (+3 Water) | 230 | Black Frost WWCC 250 | 77.38 | −4.62 ± 0.47 |
| Hop's Zacian ex JTG 111 (+4 Metal) | 230 | Brave Slash MMMC 240 | 77.30 | −4.70 ± 0.48 |
| Mega Diancie ex PFL 41 (+3 Psychic) | 270 | Garland Ray PP 120 per Energy discarded (2) | 76.21 | −5.79 ± 0.48 |
| Mega Absol ex MEG 161 (+3 Darkness) | 280 | Claw of Darkness DDC 200 + hand discard | 75.26 | −6.74 ± 0.51 |
| Mega Latias ex MEG 100 (+2 Fire, +2 Psychic) | 280 | Illusory Impulse (Fire + Psychic + C) 300, discard all | 75.15 | −6.85 ± 0.48 |
| Mega Mawile ex MEG 162 (+3 Metal) | 270 | Huge Bite MMC 260 (30 if the target is damaged) | 74.98 | −7.02 ± 0.52 |
| Pikachu ex ASC 277 (+2 G, L, M) | 200 | Topaz Bolt (Grass + Lightning + Metal) 300, discard 3 | 73.06 | −8.94 ± 0.53 |
| Raging Bolt ex TEF 123 (+3 Lightning) | 240 | Bellowing Thunder (Lightning + Fighting) 70 per Basic Energy discarded | 66.35 | −15.65 ± 0.65 |

Nothing replaces Mega Audino ex: its second accelerator is worth more than
a second hitter. Off-type attackers cost the most, because each Energy of
their type is one fewer Fighting Energy for Zygarde, and they get no help
from Fighting Gong, Premium Power Pro or Rocky Fighting Energy.

## Add: Audino kept, −1 Basic Fighting Energy (`bb_add_<card>.txt`)

| Added | 200 games | Paired | 1000 games | Paired (base 81.48%) |
|---|---|---|---|---|
| Mega Kangaskhan ex | 82.69% | +0.69 ± 0.45 | 82.51% | +1.03 ± 0.28 |
| Cornerstone Mask Ogerpon ex | 82.67% | +0.67 ± 0.52 | **83.30%** | **+1.83 ± 0.41** |
| A 3rd Mega Zygarde ex | 82.36% | +0.36 ± 0.41 | | |
| Mega Hawlucha ex | 81.90% | −0.10 ± 0.47 | | |
| Kangaskhan and Ogerpon (−2 Energy) | | | 83.50% | +2.02 ± 0.44 |

Both together against Ogerpon alone: +0.19 ± 0.26, a tie. Against the base
list head to head, both together won 44.2% and Ogerpon alone 49.3%. The
field list now adds Ogerpon only.

Results are in `summary.txt` and `results/` (`_bb2_200` and `_bbc_1000`).
