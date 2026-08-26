# Mega Chandelure ex — retreat tax

> **Superseded for the deck it was derived from.** This file read the
> retreat tax as a *damage* scaler. The user's actual plan was to use it
> as a **lock** — trap a harmless Pokémon Active and win by decking the
> opponent out — which makes the mill package the win condition rather
> than the chaff this file treats it as. See
> `chandelure_centiskorch_deck_out.md` for that build. The damage numbers
> and the Path A/B comparison below are still correct on their own terms,
> and this remains a real deck if you want to win on Prizes.

Refocus of a user-supplied Chandelure list that was running three
different win conditions out of one evolution line. This file keeps the
retreat-tax half and documents why the other two were cut.

## The payoff

**Mega Chandelure ex** (PBL 38, Stage 2 MEGA ex, 350 HP Psychic,
evolves from Lampent, retreat 2, **3 Prizes**)

- Ability **Binding Flame** — *"Your opponent's Active Pokémon's Retreat
  Cost is Colorless more."* No Active requirement, so it works from the
  Bench, and **it stacks once per copy in play**.
- Attack **Phantom Maze** — `Psychic / Psychic`, **130+**, *"this attack
  does 50 more damage for each Colorless in your opponent's Active
  Pokémon's Retreat Cost."*

The Ability inflates the exact number the attack reads. Every extra copy
on the Bench is +50 damage, for two Energy:

| Opponent's printed retreat | 1 in play | 2 in play | 2 + Gravity Gemstone |
| --- | --- | --- | --- |
| 0 | 180 | 230 | 280 |
| 1 | 230 | 280 | 330 |
| 2 | 280 | 330 | 380 |
| 3 | 330 | 380 | 430 |
| 4 | 380 | 430 | 480 |

`Boss's Orders` is a damage card here, not just a gust: you choose which
Pokémon is Active, so you drag up whichever benched Pokémon has the
biggest Retreat Cost.

## Why this path and not the other two

The original list ran **three** plans through one Litwick/Lampent line:

1. **Mega Chandelure ex** — retreat tax (this file).
2. **Chandelure TWM 38** — `Mind Ruler`, 30 damage per card in the
   opponent's hand, fed by `Alluring Light` (each player draws 1) and
   `Comfey`'s `Flower Shower` (each player draws 3).
3. **Sizzlipede / Centiskorch** — `Controlled Burn`, milling 1–2 cards off
   the opponent's deck per turn.

Both Chandelure and Mega Chandelure ex evolve from Lampent, so plans 1 and
2 were competing for the same three Litwick and three Lampent, on **two**
Rare Candy, **one** Buddy-Buddy Poffin and **zero** Ultra Ball. Measured
over 1000 trials, in play by turn 6: **Mega Chandelure ex 23.9%,
Chandelure 25.4%**. Neither payoff showed up in three quarters of games.

There was also a direct contradiction: **3 Xerosic's Machinations** cut
the opponent to 3 cards, which turns `Mind Ruler` into a **90-damage
attack**. One package was actively switching the other one off.

Both refocused builds were built and simulated head to head:

| | Scrafty | Hop's | Carbink | Decidueye | Luxray |
| --- | --- | --- | --- | --- | --- |
| original 3-plan list | 23.7% | 36.7% | 26.3% | 36.3% | 28.0% |
| **Path A — Mega Chandelure ex** | **52.7%** | **58.3%** | 50.3% | **65.3%** | **55.0%** |
| Path B — Chandelure / Mind Ruler | 58.7% | 59.2% | **54.4%** | 56.4% | 47.2% |

Head to head over 400 games, **Path A beats Path B 55.8% to 44.0%**, and
Path A beats the original list **76.7% to 22.0%**.

The averages are closer than that margin suggests, and the simulator
flatters Path B for a reason it cannot model: its generic AI does not
punish being handed free cards. Three things decide it anyway:

- **Mind Ruler's damage is under the opponent's control.** They can simply
  play their hand down to 2 and it becomes a 60-damage attack. Phantom
  Maze's number is under *yours* — Binding Flame copies, Gravity Gemstone,
  and which Pokémon you gust up. Its floor is 180; its normal range is
  230–330.
- **350 HP versus 130 HP.** Chandelure dies to essentially every attack in
  the format. Mega Chandelure ex survives most single hits.
- **Feeding a real opponent 1–3 extra cards a turn** is how Path B gets to
  its big numbers, and those cards are then used against you.

## Decklist

```
Pokémon: 19
4 Litwick PBL 36
4 Lampent PBL 37
4 Mega Chandelure ex PBL 38
3 Team Rocket's Chingling DRI 85
2 Dedenne SSP 87
1 Eevee TWM 135
1 Sylveon PRE 40

Trainer: 32
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Rare Candy MEG 125
3 Poké Pad ASC 198
3 Gravity Gemstone SCR 137
2 Air Balloon MEG 166
2 Night Stretcher MEG 173
4 Lillie's Determination MEG 119
4 Boss's Orders MEG 114
2 Hilda WHT 164

Energy: 9
2 Telepathic Psychic Energy POR 88
6 Basic Psychic Energy
1 Legacy Energy TWM 167

Total Cards: 60
```

### Card choices worth stating

- **4 Mega Chandelure ex, not 2.** Binding Flame has no Active
  requirement, and a 350 HP body is safe on the Bench, so extra copies are
  pure damage rather than dead weight. This is the deck's damage scaling.
- **Legacy Energy TWM 167 as the ACE SPEC.** *"If the Pokémon this card is
  attached to is Knocked Out ... that player takes 1 fewer Prize card."*
  On a 3-Prize Mega Evolution ex that is the single largest ACE SPEC
  effect available to this deck — it turns the deck's one real liability
  into a 2-Prize trade. It also provides every type, so it pays half of
  Phantom Maze on its own.
- **Telepathic Psychic Energy POR 88.** *"When you attach this card from
  your hand to a Psychic Pokémon, search your deck for up to 2 Basic
  Psychic Pokémon and put them onto your Bench."* Litwick is a Basic
  Psychic Pokémon, so this is an Energy attachment **and** a Buddy-Buddy
  Poffin in one card.
- **3 Gravity Gemstone SCR 137.** +1 Retreat Cost to both Actives while
  attached to yours — +50 Phantom Maze. Mega Chandelure ex never wants to
  retreat, so the drawback is free. Only one can be live at a time (one
  Tool per Pokémon, Active only), so the extra copies buy consistency.
- **Eevee TWM 135 / Sylveon PRE 40.** `Safeguard` prevents all damage from
  the opponent's Pokémon **ex** — a 120 HP wall an ex deck literally
  cannot touch. Two cards for a strong but situational tech; it only
  arrives by turn 6 in 25% of games, so treat it as a bonus, not a plan.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC, no
energy-type shortfall, no attack-gating Ability text.

Mulligan with 10 Basics: **25.9%** (the original ran 12 Basics for 19.1% —
slightly better, but it was padding the count with cards that did nothing).

1000-trial baseline, in play by turn 6:

| | % | avg turn |
| --- | --- | --- |
| Litwick | 97.2% | 1.48 |
| Team Rocket's Chingling | 93.4% | 1.59 |
| Dedenne | 82.2% | 1.88 |
| Lampent | 75.7% | 2.98 |
| **Mega Chandelure ex** | **64.4%** | 3.64 |
| Eevee | 58.7% | 2.27 |
| Sylveon | 25.0% | 3.74 |

Mega Chandelure ex by turn 6: **23.9% → 64.4%**. First attack by turn 6:
88.5%.

## What was cut, and why

| Cut | Why |
| --- | --- |
| 2 Chandelure TWM 38 | competing Stage 2 off the same Lampent; see the path comparison |
| 2 Sizzlipede / 2 Centiskorch | `Controlled Burn` mills 1–2 per turn — roughly 30 turns to deck someone. Four slots on a plan that never closes |
| 3 Xerosic's Machinations | anti-synergy with Mind Ruler, and irrelevant once Mind Ruler is gone |
| 1 Comfey | `Flower Shower` hands the opponent 3 cards; only ever wanted for Mind Ruler |
| 1 Maractus JTG 8 | `Corner` prevents retreat, which does **not** raise Retreat Cost — no Phantom Maze synergy at all |
| 1 Elgyem BLK 40 | `Slight Shift` moves an Energy between the opponent's own Pokémon; no line to it |
| 1 Latias ex SSP 239 | `Skyliner` frees your *Basics*, and this deck attacks with a Stage 2. A 2-Prize liability for mobility Air Balloon already covers |
| 1 Team Rocket's Watchtower | shuts off Colorless Abilities on both sides — narrow, and its one Stadium slot is better empty than fighting your own board |
| 1 Lana's Aid | Night Stretcher does the relevant half at Item speed and doesn't cost the Supporter |

Added: **4 Ultra Ball** (the original had none, and `Poké Pad` cannot fetch
a Rule Box Pokémon, so there was no way to search Mega Chandelure ex at
all), **Rare Candy 2 → 4**, **Buddy-Buddy Poffin 1 → 4**, **Gravity
Gemstone 1 → 3**, **Mega Chandelure ex 2 → 4**.

## Where this deck loses

- **Darkness weakness ×2** on a 350 HP body is 175 effective HP against a
  Darkness attacker, and Mega Chandelure ex gives up **3 Prizes**. Legacy
  Energy softens exactly one of those trades, once per game.
- **Air Balloon on their side.** −2 Retreat Cost drags a retreat-2 Pokémon
  to 0, and Phantom Maze with one Binding Flame drops to 180. Answer it by
  gusting a different, un-ballooned target with Boss's Orders.
- **Free-retreat Abilities** (an opposing `Latias ex`, `Comfey`-style
  effects) do the same thing more permanently and cannot be played around.
- **Stage 2 speed.** 64.4% by turn 6 is good for a Stage 2 deck but still
  means one game in three where the payoff is late.

## Simulator work this deck required

Phantom Maze and Binding Flame were both invisible to the engine before
this list was analysed, so the path comparison above could not have been
run at all:

1. **`query_retreat_modifier` only read the owner's own passives.** Retreat
   is the one stat an opponent routinely modifies from across the table,
   and Binding Flame / Ariados's Big Net are exactly that. Rewritten to
   read both sides, with an `effective_retreat` helper and a `RETREAT_TOOLS`
   table (Air Balloon −2, Rescue Board −1, Gravity Gemstone +1 to both
   Actives) that the retreat decision now uses too.
2. **`_clause_count` had no case for "for each Colorless in your
   opponent's Active Pokémon's Retreat Cost."** Phantom Maze scored as a
   flat 130 — the deck's entire damage engine was being thrown away.
   Also fixes `String Bind`, `Shadowy Knot` and `Gusting Collision`.
3. **`no_retreat_cost` dropped its "your Basic Pokémon" restriction**, so
   Latias ex's Skyliner was zeroing the Retreat Cost of Stage 2s as well.
4. **`modify_retreat` dropped Ariados's "Active Evolution Pokémon"
   restriction**, which made a conditional tax look unconditional.

All four are covered by firing tests in `test_ability_engine.py`.
