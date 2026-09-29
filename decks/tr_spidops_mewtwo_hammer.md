# Team Rocket's Spidops / Mewtwo ex / Crushing Hammer

<!-- field-results -->
> ### Field results — 2026-09-29
> **64.4% mean · 65.8% median · 50 of 56 winning matchups · rank 8 of 57**
>
> Best `static_venom_drapion` 89% · worst `tauros_risky_ruins` 34%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-09-29** and was measured against a different field or engine.
<!-- field-results -->


**Not my list.** Supplied 2026-09-29. Every Pokemon is a Team Rocket's
Pokemon, and that count is the engine: Spidops's Rocket Rush does 30 for
each of them in play (180 on a full board, +30 Brave Bangle against an
ex), Mewtwo ex cannot attack until four are in play, and Erasure Ball
throws Benched Energy for +60 each, which Spidops's Charging Up puts back
from the discard pile. Kangaskhan ex's Wicked Impact is 220 on any turn a
Team Rocket's Supporter was played (Ariana, Proton, Giovanni, Petrel,
Archer, all fetched by Transceiver). Crushing Hammer strips Energy;
Nighttime Mine taxes Tera attackers; Articuno is there for Repelling Veil
(its Water attack is unpayable here, which is fine).

**64.09% (±0.20) against the 56-deck field, 1000 games per opponent,
winning 51 of 55.** Worst: Mega Excadrill drill mill 31.7, Tauros Risky
Ruins 32.9, Mega Chandelure retreat tax 43.9. Best: Wobbuffet/Orbeetle
88.4, Static Venom Drapion 87.4, Festival Lead 84.1.

1000-trial baseline: Tarountula in play by turn 6 in 95.3% (avg turn
1.82), Spidops 76.6% (avg 3.33), first attack by turn 6 in 84.0% (avg
3.03).

## What the engine got wrong (fixed, with regression tests)

- **Brave Bangle added 60, not 30**, and ignored its ex-only clause: the
  generic Tool reader and DAMAGE_TOOLS both priced it. Rocket Rush hit for
  240 off a six-Pokemon board. This list measured 65.13% before the fix.
  Four other field decks run Bangle and dropped 1.4 to 4.8 points.
- Crushing Hammer worked but logged nothing, which read as a dead card in
  the play tally. It logs its discard now.

## Tested (200 games x 55 opponents, paired)

Replacing the 2 Mimikyu (whose Tera-copy attack was never used in 48
logged games): 2 Murkrow -0.63, 2 Wobbuffet -0.48, 2 Zapdos -1.54. None
beat it: Mimikyu is a 60 HP, zero-retreat Team Rocket's body that counts
for Spidops and Mewtwo. The list stays as supplied.

## PTCGL import

Three printings are outside this Standard pool (Crushing Hammer UPR 166,
Energy Switch SIT 212, Ultra Ball BRS 186); the import uses legal
reprints of the same cards. The DRI numbers are right -- this pool files
them under their ASC reprints.

```
Pokémon: 15
2 Team Rocket's Articuno DRI 51
1 Team Rocket's Mewtwo ex DRI 213
4 Team Rocket's Spidops DRI 20
2 Team Rocket's Mimikyu ASC 238
4 Team Rocket's Tarountula ASC 18
1 Team Rocket's Kangaskhan ex ASC 162
1 Team Rocket's Sneasel DRI 128

Trainer: 35
1 Energy Search POR 72
2 Team Rocket's Giovanni DRI 238
2 Lillie's Determination MEG 184
1 Secret Box TWM 163
3 Crushing Hammer POR 71
1 Team Rocket's Archer DRI 223
1 Team Rocket's Giovanni DRI 225
1 Brave Bangle PBL 104
1 Nighttime Mine ASC 197
3 Team Rocket's Proton DRI 227
4 Team Rocket's Ariana DRI 237
2 Team Rocket's Factory DRI 173
1 Team Rocket's Transceiver DRI 178
1 Energy Switch MEG 115
2 Night Stretcher SSP 251
3 Ultra Ball MEG 131
1 Poké Pad POR 113
1 Prism Tower CRI 111
1 Team Rocket's Petrel DRI 226
3 Team Rocket's Transceiver ASC 263

Energy: 10
6 Basic Grass Energy
4 Team Rocket's Energy DRI 182

Total Cards: 60
```
