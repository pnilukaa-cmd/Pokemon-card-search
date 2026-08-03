# Darkness Hand-Lock / Mill

A control deck built around unconditional hand disruption (Sandile/Krokorok/Krookodile's
`Tighten Up`), deck drawdown/mill (Deino/Zweilous/Hydreigon ex's `Stomp Off` /
`Crashing Headbutt`), and a hard-to-kill 330 HP attacker core (Hydreigon ex, Mega Scrafty ex).

## Centerpieces

1. **Hydreigon ex** (Surging Sparks) — 330 HP. `Crashing Headbutt` costs just Darkness+Colorless
   (2 energy) for 200 damage and mills 3 cards off the top of the opponent's deck. Best
   damage-per-energy in the deck, doubles as the mill win condition.

2. **Krookodile** (Black Bolt) — `Tighten Up` unconditionally discards 2 cards from the
   opponent's hand every attack, no coin flip, no condition. Stacked with `Xerosic's
   Machinations` (discard to 3) in the same turn, this can put the opponent down to 1 card
   in hand by turn 3-4. `Cursed Slug` finishes for 240 damage once their hand is that low.

3. **Mega Scrafty ex** (Ascended Heroes) — 330 HP. `Outlaw Leg` hits both resources at once:
   160 damage + discard 1 random hand card + mill 1 deck card. Ability `Counterattacking
   Crest` punishes anything that attacks it with 5 damage counters, discouraging trades.

## Design notes

- Runs 3 evolution engines (Krookodile / Hydreigon / Mega Scrafty), which trades some
  consistency for redundancy and threat variety. A more consistent build would cut one line.
- 4x Rare Candy means the Stage 1 bridge cards (Krokorok, Zweilous) are kept at 1 copy each
  — they're insurance for when Candy isn't drawn, not the primary path.
- Waitress / Energy Search replaced Crispin: Crispin requires finding 2 *different* Basic
  Energy types, which doesn't work in a mono-Darkness deck.
- Max Rod (ACE SPEC) was chosen over Prime Catcher because this deck's win condition is a
  long grindy mill/disruption game — recursion (up to 5 Pokémon/Energy back from discard)
  matters more here than an extra tempo/gust effect.
- Checked with `check_energy_support.py`: this exact printing of Hydreigon ex (`sv8-119`) also
  has a second attack, `Obsidian` (Psychic/Darkness/Metal/Colorless, 130 damage), which this
  mono-Darkness deck can never pay for. That's fine — the deck was never built around it,
  `Crashing Headbutt` (Darkness/Colorless) is the intended attack — but it's worth stating
  plainly rather than leaving `Obsidian` as a silent dead line on the card.

## Pokémon TCG Live Import

```
Pokémon: 14
2 Sandile BLK 57
1 Krokorok BLK 58
2 Krookodile BLK 59
2 Deino SSP 117
1 Zweilous SSP 118
2 Hydreigon ex SSP 119
2 Scraggy ASC 134
2 Mega Scrafty ex ASC 135

Trainer: 34
4 Boss's Orders MEG 114
2 Waitress ASC 215
2 Energy Search POR 72
2 Xerosic's Machinations SFA 64
2 Lacey SCR 139
1 Eri TEF 146
4 Ultra Ball MEG 131
4 Rare Candy MEG 125
3 Buddy-Buddy Poffin TEF 144
3 Night Stretcher SFA 61
2 Hand Trimmer TEF 150
2 Air Balloon BLK 79
2 Rescue Board TEF 159
1 Max Rod PRE 116

Energy: 12
12 Basic Darkness Energy

Total Cards: 60
```
