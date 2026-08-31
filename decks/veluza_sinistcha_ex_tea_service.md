# Veluza / Sinistcha ex — "tea service"

Answer to "can you combine Kofu and Sinistcha?" **Yes, and it is a
markedly better deck than the pure Food Prep build — but not for the
reason it looks like.** The two engines do not combo. They coexist,
because of a cost-symbol coincidence, and Sinistcha ex happens to fix the
exact weakness Food Prep has.

## They do not share a payoff

Worth stating plainly, because it is the first thing you would assume:

- **`Food Prep` exists on exactly two cards** — `Crabominable` and
  `Veluza`. `Sinistcha ex` does not have it, so **Kofu discounts nothing
  on Sinistcha**.
- `Re-Brew` counts **Basic Grass Energy in your discard pile**. Kofu puts
  cards on the **bottom of your deck**, not the discard, so **Kofu does
  not fuel Re-Brew** either.
- They actively **compete** for `Brilliant Blender`. It discards five
  cards, once, and those five are either Kofu (turning on Food Prep) or
  Grass Energy (loading Re-Brew). Split 4/1 and you get a free Sonic Edge
  and a 20-damage Re-Brew; neither is fully on.

## What actually makes it work

Three cost lines, all of which happen to be Colorless:

| Attack | Cost | Effect |
| --- | --- | --- |
| `Veluza` — Sonic Edge | `C C C C` → **free** at 4 Kofu | 110, *damage unaffected by effects on their Active* |
| **`Sinistcha ex` — Re-Brew** | **`C`** | 2 damage counters **anywhere** per Basic Grass Energy in your discard |
| `Sinistcha ex` — Matcha Splash | `G C` | 120, heal 30 from each of your Pokémon |

Because Sonic Edge is **all-Colorless** and Re-Brew is **one Colorless**,
a single **Basic Grass Energy** line pays for both attackers *and* is
Re-Brew's ammunition once it reaches the discard. That is the whole
bridge: the Energy does double duty, not the Kofu.

And Re-Brew costing **one** Energy is what fixes the Food Prep deck's real
problem. The pure build cannot attack until Kofu land — first attack by
turn 6 in only 53.1% of games. Here it is **73.8%**, because Sinistcha ex
can attack on turn 2 regardless of whether the discount is online yet.

`Crabominable` comes out. Haymaker is the only attack in either shell that
needs a real **Water** symbol, and dropping it is what lets the deck go
mono-Grass.

## Decklist

```
Pokémon: 18
4 Veluza SCR 45
3 Poltchageist TWM 171
3 Sinistcha ex TWM 189
3 Dunsparce JTG 120
3 Dudunsparce PRE 80
1 Fezandipiti ex ASC 142
1 Shaymin DRI 10

Trainer: 34
4 Kofu SCR 138
4 Team Rocket's Petrel ASC 207
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
4 Poké Pad ASC 198
3 Team Rocket's Factory ASC 203
2 Lillie's Determination MEG 119
2 Boss's Orders MEG 114
2 Switch MEG 130
2 Brave Bangle WHT 80
1 Brilliant Blender SSP 164
1 Night Stretcher MEG 173
1 Redeemable Ticket JTG 156

Energy: 8
8 Basic Grass Energy

Total Cards: 60
```

### Card choices worth stating

- **`Poltchageist` TWM 171, not TWM 21.** `Storehouse Hideaway`: *"As long
  as this Pokémon is on your Bench, prevent all damage from and effects of
  attacks from your opponent's Pokémon done to this Pokémon."* A 30 HP
  Basic that cannot be sniped off the Bench, so the Sinistcha ex line
  cannot be pre-emptively broken. It is also **Poffin-eligible** at 30 HP.
  TWM 21's `Tea Server` pulls Grass Energy *out* of the discard, which is
  the wrong direction entirely — it un-loads Re-Brew.
- **`Ultra Ball` is a fuel line here**, not just search. Its cost is
  discarding 2 cards from hand, and both things this deck wants in the
  discard — Kofu and Grass Energy — are legal discards.
- **Re-Brew consumes its own ammunition** (*"then, shuffle those Energy
  cards into your deck"*). It is a burst, not an engine: one big hit, then
  you re-load. Plan the turn you fire it.
- **`Brave Bangle` only helps Veluza.** Sinistcha ex has a Rule Box, so
  the Bangle's no-Rule-Box clause excludes it.
- **`Redeemable Ticket` stays** — with 4 Kofu and a one-of Blender, 42.1%
  of games prize something the engine needs, and Ticket rerolls the pile.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC, no
energy-type shortfall, no attack-gating Ability text. Mulligan **19.1%**
(12 Basics).

1000-trial baseline, in play by turn 6:

| | % | avg turn |
| --- | --- | --- |
| Poltchageist | 98.7% | 1.60 |
| Dunsparce | 96.0% | 1.65 |
| Veluza | 95.5% | 1.75 |
| **Sinistcha ex** | **65.6%** | 3.54 |
| Dudunsparce | 63.5% | 3.55 |

**First attack by turn 6: 73.8%**, against 53.1% for the pure Food Prep
build — a 21-point gain, and the single most important number here.

Full field, 29 decks, 150 games each:

| | mean | median | winning |
| --- | --- | --- | --- |
| pure Food Prep (`crabominable_veluza_food_prep`) | 59.5% | 56.0% | 21/29 |
| **this build** | **65.3%** | **64.0%** | **26/29** |

It beats the deck it came from **60.0%** head to head. Best matchups:
Eerie Inferno 88.0%, T.R. Wobbuffet 86.0%, Darkness mill 85.3%, Chandelure
mill 78.7%. Worst: Panic Poison Paralysis 33.3%, Steven's Carbink 42.7%,
Lurantis heal punish 49.3%.

## Where it loses

- **Speed decks still beat it** (Panic Poison 33.3%). Turn-2 Re-Brew off
  an empty discard places almost nothing; the deck is only *less* slow
  than the Food Prep build, not fast.
- **Flat damage reduction** (Steven's Carbink 42.7%) — though Sonic Edge's
  *"damage isn't affected by any effects on your opponent's Active"* is
  specifically the out, and Re-Brew places **counters**, which most −30
  effects do not stop either. The loss is more about clock than about the
  wall.
- **Healing** (Lurantis 49.3%) undoes placed counters, same as it undoes
  every damage-placement deck.
- **Sinistcha ex is 2 Prizes**, which partly gives back the single-Prize
  advantage the Food Prep shell had.
- **The Blender is one card and does one job.** Whichever engine you point
  it at, the other one starts cold.

## Simulator work this deck required

`Re-Brew` compiled to a **flat 2 damage counters**, dropping *"for each
Basic Grass Energy card in your discard pile"* — reading a 100+ damage
attack as a 20-damage one. Same bug class as Food Prep's discount. Adds a
`place_counters_per_discard` rule that carries the counted card type and a
`consumes_fuel` flag for the shuffle-back clause, plus runtime that counts
the fuel, places the damage and then spends it.

Also: `attack_rider_value` was pricing Re-Brew at a flat 20 regardless of
the discard, so the AI could not tell a loaded Re-Brew from an empty one;
and `Brilliant Blender` was hard-coded to search out Kofu, making it a
blank in any deck with a different discard payoff. Both now read what the
board actually counts.
