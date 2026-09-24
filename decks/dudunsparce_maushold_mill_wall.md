# Dudunsparce / Maushold mill wall

**Not my list.** Supplied 2026-09-24 as the winner of a large tournament.
Every line resolves to the card pool; `Basic {P} Energy MEE 13` is written
here as `Basic Psychic Energy`, as for every Basic Energy in this repo.

**38.05% (±0.20) against all 54 field decks at 1000 games each, winning 11.**
Measured on the engine as of this commit.
That is well below what a tournament win implies, and the gap is read as
the pilot's, not the list's: see "Still missing".

```
Pokémon: 19
3 Dudunsparce TEF 129
4 Dunsparce JTG 120
1 Dudunsparce ex JTG 121
1 Elgyem BLK 40
3 Maushold 30C 125
1 Fan Rotom SCR 118
1 Maushold SSP 158
4 Tandemaus SSP 157
1 Shaymin DRI 10

Trainer: 33
3 Battle Cage PFL 85
4 Poké Pad ASC 198
4 Night Stretcher ASC 196
3 Dark Bell PBL 75
1 Sacred Ash DRI 168
1 Lana's Aid TWM 155
2 Hilda WHT 84
1 Redeemable Ticket JTG 156
3 Gravity Gemstone SCR 137
4 Buddy-Buddy Poffin ASC 184
4 Lillie's Determination MEG 119
2 Boss's Orders ASC 183
1 Neutralization Zone SFA 60

Energy: 8
4 Basic Psychic Energy
4 Mist Energy TEF 161

Total Cards: 60
```

## The plan

- **Win condition: mill.** Three `Maushold 30C 125` (Gnaw Together: a coin
  per Maushold in play, 2 cards off the opponent's deck per heads) and one
  `Maushold SSP 158` (Familial March: two more Maushold straight onto the
  Bench).
- **Walls.** `Neutralization Zone` (no damage from Pokemon ex to anything
  without a Rule Box, both sides), `Shaymin` (Bench immune to attack
  damage), `Battle Cage` (no effect counters on the Bench), `Mist Energy`
  (no attack effects on its holder).
- **Lock.** `Boss's Orders` drags up something that cannot attack,
  `Gravity Gemstone` adds a Colorless to both Actives' Retreat Cost, `Dark
  Bell` Confuses both Actives -- cured on your own side by evolving.
- **Engine that does not deck itself.** `Dudunsparce`'s Run Away Draw draws
  3 and shuffles itself back in; `Sacred Ash`, `Lana's Aid` and `Night
  Stretcher` recycle; `Redeemable Ticket` re-rolls the Prizes.

## What the engine had wrong

Six of its cards were compiled and never used. Each fix measured paired
against the same field at 200 games (tag `zg`):

| fix | paired effect |
|---|---:|
| Neutralization Zone / Battle Cage are played; Bench damage is checked against Shaymin and the Zone; Battle Cage stops counters, not attack damage | +2.58 ± 0.84 |
| a mill deck gusts up a Pokemon that can neither attack nor retreat, and holds the gust while the Active is stuck; Dark Bell is not played into your own attacker | +2.67 ± 0.60 |
| Dark Bell guard counts the Energy still in hand (Items resolve before the attach) | +0.84 ± 0.62 |
| Fan Call fires ("once during your first turn" was read as passive) and fetches only Colorless | +1.64 ± 0.60 |

Measured and **reverted**: feeding Energy to Maushold first (-0.18 ± 0.82)
and pricing Familial March by future mill (-0.93 ± 0.55).

Fixing the inert-card guard to test what the pilot actually plays found the
same two Stadiums dead in eleven decklists, and `Nighttime Mine` dead in one.

## Still missing

The mill is too slow. In losses the opponent still has ~24 cards in deck;
Maushold rarely reach three in play, never four, and Gnaw Together is the
chosen attack on ~16% of turns. Most losses are six Prizes taken. The walls
are in play far less than a real player would keep them: three Battle Cage
to one Neutralization Zone, and the opponent's own Stadium bumps them.

Best and worst matchups (1000 games):

| opponent | win % |
|---|---:|
| `study_centiskorch_bastiodon_mill` | 89.9 |
| `feraligatr_munkidori_damage_transfer` | 80.7 |
| `study_flygon_sandy_flapping_mill` | 77.7 |
| `team_rockets_wobbuffet_orbeetle_damage_launder` | 63.0 |
| `meta_festival_lead` | 62.0 |
| `meta_ns_zoroark` | 59.6 |
| ... | |
| `cradily_accelgor_conditions` | 20.3 |
| `cradily_amoonguss_conditions` | 20.1 |
| `ns_zoroark_night_joker_toolbox` | 18.8 |
| `lurantis_heal_punish` | 15.8 |
| `wugtrio_paralysis_pin` | 15.1 |
| `panic_poison_paralysis` | 13.7 |

1000-trial baseline: Maushold (Gnaw) in play by turn 6 in 61.0% (avg turn
3.06), Familial March Maushold 25.8%, first attack by turn 6 94.6%.
