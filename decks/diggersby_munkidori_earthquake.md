# Diggersby Earthquake / Munkidori / Mega Darkrai ex

Built 2026-10-07 around Diggersby POR 65's **Earthquake**: 140 damage for
ONE Colorless Energy, plus 30 to each of your own Benched Pokemon.

**66.09% (±0.17) against the 64-deck field, 1000 games per opponent,
winning 52 of 63.** Beats Tauros (field #1) 65%. Worst: N's Zoroark 32,
Raging Bolt 36, Ditto Transform 38, Team Rocket's Spidops 39, Persian ex 41.

## Why it works: the drawback is the engine
- **Munkidori**, Adrena-Brain (needs any Darkness Energy attached): moves up to 3 damage counters from one of your Pokémon to one of theirs. Earthquake puts exactly 3 counters on each Benched Pokémon, so each Munkidori turns that self-damage into **+30 on their board** and heals yours.
- **Mega Darkrai ex**, Dusk Raid (DD): 110, **+110 if your Benched Pokémon have damage counters**. Earthquake guarantees that, so it's 220 for two Energy as the second attacker. It's a Mega ex, so it gives up 3 Prizes when Knocked Out.
- **One Energy type:** 10 Darkness. Diggersby's Earthquake takes anything, Munkidori needs Darkness, and so does Darkrai.

## Turns
- **Turn 1:**
  1. Poffin for Bunnelby ×2, and bench Munkidori.
  2. Attach Darkness to Munkidori. You can't evolve on your first turn.
- **Turn 2:**
  1. Evolve to Diggersby, attach, and Earthquake for 140.
  2. Your Bench takes 30 each.
  3. Next turn, Adrena-Brain moves those 30s onto the opponent.
- **Retreat:** Diggersby has Retreat Cost 4, so pivot with Switch (4) or Air Balloon.

1000-trial development baseline: Bunnelby in play by turn 6 in 98% of games (average turn 1.4), Diggersby 93% (2.7), Munkidori 93% (1.9). First attack by turn 6 in 91% (average turn 2.9).
Mulligan rate: 30% (9 Basics). Adding 2 Fan Rotom to cut it measured −6.1.

## Engine fix this deck exposed
The pilot never attached Energy to a Pokémon whose **Ability** needs it.
Munkidori's attack is unpayable here, so Adrena-Brain ran 2 times in
78 Earthquakes. Feeding Ability-gated Pokémon measured positive on all 8
Munkidori decks in the field (+0.4 to +10.4), and is now on by default.

## PTCGL import

```
Pokémon: 13
4 Bunnelby POR 64
4 Diggersby POR 65
3 Munkidori ASC 99
2 Mega Darkrai ex PBL 101

Trainer: 37
4 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Hilda WHT 84
1 Team Rocket's Petrel ASC 207
1 Lana's Aid TWM 155
3 Pokégear 3.0 BLK 84
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Poké Pad ASC 198
4 Switch MEG 130
3 Night Stretcher MEG 173
2 Energy Switch MEG 115
2 Air Balloon MEG 166
1 Hero's Cape TEF 152

Energy: 10
10 Basic Darkness Energy

Total Cards: 60
```
