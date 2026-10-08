# Team Rocket's Golbat / Crobat ex counters + Brute Bonnet

<!-- field-results -->
> ### Field results — 2026-10-08
> **48.8% mean · 45.7% median · 32 of 76 winning matchups · rank 45 of 77**
>
> Best `mew_baby_box` 93% · worst `lurantis_heal_punish` 17%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-10-08** and was measured against a different field or engine.
<!-- field-results -->

Built 2026-10-08 as a faster answer to the Trevenant/Uxie spread list
(37.4%), which needs several turns of spreading before it threatens
anything. This deck puts a few counters on the opponent's **Active**
for free (evolution Abilities, not attacks), then cashes them in with a
per-counter attacker the same turn.

**53.03% (±0.18) against the 66-deck field, 1000 games per opponent,
winning 34 of 65.** Beats the Trevenant list 67-33. Worst: N's Zoroark 18,
Maushold mill 24, Lurantis 24, Ditto Transform 26, Wugtrio 27. Best: Mew
Baby Box 93, Static Venom Drapion 92, Mew Pikachu box 90.

## The engine
- **Free counters (Abilities, no attack used):**
  - Team Rocket's Golbat, Sneaky Bite: 2 counters on any opposing Pokemon when you evolve into it.
  - Team Rocket's Crobat ex, Biting Spree: 2 counters on each of 2 opposing Pokemon when you evolve into it. Its attack, Assassin's Return (DD, 120), can put it back in your hand to evolve again next turn.
- **Payoff:** Brute Bonnet (Basic, 120 HP), Relentless Punches (DDD): 50 + 50 per counter on their Active. It averaged 250 in logged games.
- **Follow-up:** Yveltal's Corrosive Winds (D): 2 more counters on every opposing Pokemon that already has some.
- **Energy:** Janine's Secret Art attaches 2 Basic Darkness from the deck to Darkness Pokemon, which covers Brute Bonnet's DDD.
- **Bulk:** Ancient Booster Energy Capsule gives Brute Bonnet (Ancient) +60 HP and blocks Special Conditions.

## A typical turn
1. Turn 1: Poffin for Zubat x2. Bench Brute Bonnet and attach Darkness.
2. Turn 2: Janine's Secret Art (2 Darkness onto Brute Bonnet). Evolve Zubat into Golbat: 2 counters on their Active. Relentless Punches for 150.
3. Turn 3 on: Golbat into Crobat ex (or Rare Candy Zubat into Crobat ex): 4 counters, so 250 or more.

## How it was tuned (200 games x 65 opponents, paired)
| Change | Result |
|---|---|
| First draft | 45.35% |
| +1 Crobat ex, +2 Rare Candy (-1 Yveltal, -2 Energy Switch) | +4.63 ± 0.65 |
| +2 Ancient Booster Energy Capsule | +2.83 ± 0.77 |
| +3 Janine's Secret Art (-2 Transceiver, -1 Petrel) | +2.52 ± 0.58 |
| All three | **+8.92 ± 1.04 (54.27%)** |

A Team Rocket's Arbok spread version (30 to every Pokemon) measured 34.6%.

1000-trial development baseline: Zubat in play by turn 6 in 98% of games (average turn 1.4), Brute Bonnet 86% (1.8), Golbat 77% (3.0), Crobat ex 42% (3.9). First attack by turn 6 in 94% (average turn 2.6).
Mulligan rate: 30% (9 Basics).

## PTCGL import

```
Pokémon: 15
4 Team Rocket's Zubat DRI 120
4 Team Rocket's Golbat DRI 121
2 Team Rocket's Crobat ex DRI 122
4 Brute Bonnet TWM 118
1 Yveltal SFA 35

Trainer: 33
4 Lillie's Determination MEG 119
3 Boss's Orders MEG 114
3 Janine's Secret Art SFA 59
2 Team Rocket's Proton ASC 208
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
2 Poké Pad ASC 198
2 Night Stretcher MEG 173
2 Switch MEG 130
2 Air Balloon MEG 166
2 Rare Candy MEG 125
1 Hero's Cape TEF 152
2 Ancient Booster Energy Capsule TEF 140

Energy: 12
12 Basic Darkness Energy

Total Cards: 60
```
