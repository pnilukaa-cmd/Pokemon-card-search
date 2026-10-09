# Hydreigon / Grafaiai Energy denial (submitted list)

A list submitted for study on 2026-10-09, kept in the field as submitted with
one change: **Rare Candy SVI 191 is a rotated printing, so it is listed as
Rare Candy MEG 125** (same card text).

**47.11% against the 80-deck field at 1000 games per opponent** (median
47.3%, 34 winning matchups), about 50th of 78 in the 2026-10-08 round robin.
Two tuned versions, 1000 games each, paired against this list:
- **[1-1 Grafaiai stall-and-mill](hydreigon_grafaiai_stall_mill.ptcgl.txt):
  61.19% (+14.08 ± 1.00, better on 78 of 80).** Keeps one Grafaiai for
  Mischievous Painting; 10 Darkness Energy, 4-4-3 Hydreigon.
- **[No Grafaiai](hydreigon_relicanth_hammer_denial.md): 63.56% (+16.45 ± 1.00,
  better on 78 of 80).**

## Plan

As the submitter describes it: strip the opponent's Energy, then put it back
on their board where it can't be used. That means a Pokémon not meant to
attack, the wrong type, or a mismatched place. That stalls them while
Zweilous's Stomp Off mills 2 a turn. The simulator agrees the deck wins by
milling: 31 of its 47 wins in 120 logged games were deck-outs.

Hydreigon 30C 99 strips Energy (Three-Headed Bite) or hits for 140
(Pitch-Black Fangs). Relicanth's Memory Dive gives every evolved Pokémon
Deino's and Zweilous's Stomp Off (mill 1 or 2).

The deck also strips Energy with Trainers:
- 4 Crushing Hammer
- Enhanced Hammer
- Rust Syndicate Grunt
- 2 Handheld Fan

**Grafaiai SSP 121** has two attacks:
- **Mischievous Painting** (C): attach up to 3 Energy from the opponent's
  discard pile to their Pokémon.
- **Energized Graffiti** (DD): 40 damage for each Energy on the opponent's
  side.

## What the simulator found

- **The setup is slow.** With 3-2-2 Hydreigon and one Rare Candy, Hydreigon is
  in play by turn 6 in 23-27% of games.
- **Six Energy is too few.** In a logged game against Dragapult, Pecharunt ex
  sat Active for three turns with at most one Energy, and Hydreigon came Active
  and never attacked.
- **The simulator put the Energy in the wrong place (fixed).** Painting put
  every Energy on the opponent's Active as Colorless. The Fan gave the moved
  Energy to the first Benched Pokémon, often the next attacker. Both now pick
  the Pokémon that can use it least, such as Budew rather than Dreepy against
  Dragapult. Worth +1.27 ± 0.51 to this list.
- **Spending Grafaiai's attack on Painting still doesn't pay.** Valued per
  Energy it parks, it measured −1.9 to −3.7. Valued only for Energy with
  nowhere useful to go, it measured −0.04 and −0.52. The stall that measures
  comes from Crushing Hammer, Handheld Fan and having the Energy to Stomp Off
  every turn.
- **Fewer Grafaiai measures better.** The 2-2 line at 10 Energy scores 57.08%,
  1-1 61.19%, none 63.56%.

Each change measured on its own (before the fix): cutting Grafaiai +7.0,
8 Energy +4.2, a third Hydreigon with a second Rare Candy +1.7. The full
tables are in the [tuned list's notes](hydreigon_relicanth_hammer_denial.md).

**Matchups (1000 games):**
- **Worst:** Lurantis 10.7%, Nidoking ex / Nidoqueen 11.3%, Raticate rush 13.4%,
  Diggersby 13.7%, Tauros 13.8%, Cradily / Amoonguss 18.6%.
- **Best:** Mew / Pikachu box 94.3%, Mew baby box 89.7%, Salazzle ex / Muk
  88.0%.

## 1000-trial setup baseline

| Pokémon | in play by turn 6 | average turn |
|---|---|---|
| Deino | 92.9% | 1.70 |
| Zweilous | 46.8% | 3.29 |
| Hydreigon | 27.1% | 4.06 |
| Shroodle | 71.4% | 2.02 |
| Grafaiai | 33.0% | 3.41 |
| Dunsparce (TEF) | 58.1% | 2.20 |
| Dunsparce (JTG) | 72.9% | 2.13 |
| Dudunsparce | 24.7% | 3.56 |
| Relicanth | 25.0% | 2.05 |
| Pecharunt ex | 26.0% | 2.06 |
| Shaymin | 29.4% | 2.33 |
| Psyduck | 39.1% | 2.02 |

First attack by turn 6 in 78.5% of games (average turn 2.77). Not modeled in
the baseline: Crushing Hammer, Enhanced Hammer, Lana's Aid, Prime Catcher,
Rust Syndicate Grunt.

**Checks:** 60 cards, no card over 4 copies, one ACE SPEC (Prime Catcher),
mulligan 19.1%. The one warning is Relicanth's Razor Fin (Fighting), which
can never be paid; Relicanth is there for Memory Dive.

## PTCGL import

```
Pokémon: 20
2 Zweilous SSP 118
3 Deino SSP 117
1 Dunsparce TEF 128
2 Dudunsparce TEF 129
2 Dunsparce JTG 120
2 Grafaiai SSP 121
2 Shroodle SSP 120
2 Hydreigon 30C 99
1 Pecharunt ex SFA 39
1 Shaymin DRI 10
1 Relicanth TEF 84
1 Psyduck ASC 39

Trainer: 34
1 Enhanced Hammer TWM 148
1 Team Rocket's Petrel DRI 176
1 Xerosic's Machinations SFA 64
4 Crushing Hammer POR 71
1 Prime Catcher TEF 157
4 Poké Pad ASC 198
2 Night Stretcher ASC 196
1 Nighttime Mine ASC 197
1 Air Balloon BLK 79
2 Handheld Fan TWM 150
1 Lana's Aid TWM 155
1 Hilda WHT 84
1 Rust Syndicate Grunt PBL 81
1 Janine's Secret Art SFA 59
4 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination MEG 119
3 Boss's Orders MEG 114
1 Rare Candy MEG 125

Energy: 6
6 Basic Darkness Energy

Total Cards: 60
```
