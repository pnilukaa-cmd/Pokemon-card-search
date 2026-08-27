# N's Zoroark ex — Night Joker toolbox

One attacker, a Bench full of borrowed attacks, and two different ways to
win. Built for setup speed: there is exactly **one evolution step in the
whole deck**, and every other Pokémon is a Basic that never evolves.

## The engine

**N's Zoroark ex** (ASC 137, Stage 1, 280 HP Darkness, from N's Zorua)

- Ability **Trade** — discard a card, draw 2. Once per turn **per copy**,
  so a second one on the Bench doubles it, and it never touches the
  Supporter slot.
- Attack **Night Joker** — `Darkness / Darkness`: *"Choose 1 of your
  Benched N's Pokémon's attacks and use it as this attack."*

Night Joker pays **two Darkness Energy** and ignores the borrowed attack's
own cost. That is the whole deck. The Bench is a menu:

| Borrowed from | Attack | What it does |
| --- | --- | --- |
| **N's Reshiram** ASC 154 | Virtuous Flame | **170**, no drawback — the every-turn workhorse |
| **N's Zekrom** ASC 155 | Rampaging Thunder | **250**, but locks you out of attacking next turn |
| **N's Zekrom** ASC 155 | Shred | 70 whose *"damage isn't affected by any effects on your opponent's Active"* — the answer to −30 walls |
| **N's Sigilyph** JTG 64 | **Victory Symbol** | *"If you use this attack when you have exactly 1 Prize card remaining, **you win this game**."* |
| **N's Purrloin** JTG 96 | Thieving Swipe | 30, and put a card from their hand on the bottom of their deck |
| **N's Joltik** JTG 49 | Zapping Short | discards all Tools from their Active first — kills Air Balloon, Maximum Belt |

The elegant part: `Virtuous Flame` costs `Fire/Fire/Lightning/Colorless`
and `Victory Symbol` costs `Psychic/Colorless/Colorless`. **Neither is
castable in this deck** — it runs nothing but Darkness Energy. They are
only ever borrowed. `check_energy_support.py` flags eight attacks here as
IMPOSSIBLE and every one of those flags is correct and irrelevant; the
copy is the point.

## The two win conditions

1. **The prize race.** 170 a turn off two Energy, or 250 when you need to
   punch through something big.
2. **N's Sigilyph's Victory Symbol.** At **exactly 1 Prize remaining** you
   stop needing to Knock anything out — you attack for two Darkness and
   win, through a 350 HP Mega, through a wall, through anything.

Victory Symbol is **insurance, not a plan**. Reaching exactly 1 Prize
means steering the count: two 2-Prize KOs plus one 1-Prize KO puts you
there, whereas three 2-Prize KOs just wins normally at 0. When the last
Prize is the hard one — they have nothing reachable, or a body you cannot
break — this is the card that ends it. `Boss's Orders` at 4 copies is
partly there to pick which Prize value you take.

## Decklist

```
Pokémon: 17
4 N's Zorua ASC 136
4 N's Zoroark ex ASC 137
3 N's Reshiram ASC 154
2 N's Sigilyph JTG 64
2 N's Zekrom ASC 155
1 N's Purrloin JTG 96
1 N's Joltik JTG 49

Trainer: 32
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
4 Poké Pad ASC 198
4 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
2 Janine's Secret Art SFA 59
2 N's PP Up ASC 195
2 N's Castle JTG 152
2 Night Stretcher MEG 173
2 Carmine TWM 145
2 Hilda WHT 164
1 Master Ball TEF 153

Energy: 11
11 Basic Darkness Energy

Total Cards: 60
```

### Card choices worth stating

- **N's Castle JTG 152** is not filler — it is the second most important
  card in the deck. *"N's Pokémon in play have no Retreat Cost."*
  Zoroark ex has printed retreat 2, and the deck's whole pattern is
  loading a spare Zoroark ex on the Bench and swapping it in the moment
  the Active one falls. Adding it to the simulator moved every matchup by
  **9–17 points** (see below) — it is that load-bearing.
- **Janine's Secret Art SFA 59** — *"Choose up to 2 of your Darkness
  Pokémon. For each, search your deck for a Basic Darkness Energy and
  attach it."* Night Joker costs exactly two Darkness, so one Janine's is
  one fully armed attacker straight out of the deck. Attach to the
  **Bench**, not the Active — attaching to your Active Poisons it — then
  bring it in for free under N's Castle. That two-card interaction is the
  deck's real setup line.
- **N's PP Up ASC 195** — recycles a Basic Energy from the discard onto a
  Benched N's Pokémon. This is the answer to losing an armed Zoroark ex.
- **Poké Pad ASC 198 at 4** — searches any Pokémon *without* a Rule Box,
  which is the entire toolbox (Sigilyph, Reshiram, Zekrom, Purrloin,
  Joltik) but not Zoroark ex. `Master Ball` and `Ultra Ball` cover that.
- **Every Basic is a Bench sitter.** Bench is 5, and the toolbox is
  exactly Bench-sized: Sigilyph, Reshiram, Zekrom, plus a spare Zorua or
  Zoroark ex.

## Numbers

`check_energy_support.py`: 60 cards, no card over 4 copies, 1 ACE SPEC.
(Eight IMPOSSIBLE flags, all on borrowed-only attacks — see above.)

Mulligan with **13 Basics: 16.3%** — the lowest of any deck in this repo.

1000-trial baseline, in play by turn 6:

| | % | avg turn |
| --- | --- | --- |
| N's Zorua | 98.4% | 1.46 |
| **N's Zoroark ex** | **82.1%** | 2.95 |
| N's Sigilyph | 76.6% | 2.06 |
| N's Reshiram | 75.3% | 2.04 |
| N's Purrloin | 56.9% | 2.11 |
| N's Zekrom | 54.8% | 2.16 |
| N's Joltik | 54.3% | 2.08 |

First attack by turn 6: **91.1%**. That 82.1% is the highest main-attacker
figure in this repo — Decidueye ex reaches 68.3%, Mega Chandelure ex
64.4%, Chandelure 61.7%. One evolution step is the entire reason.

`simulate_versus.py`, 250 games each:

| Opponent | before N's Castle was modeled | with it |
| --- | --- | --- |
| Mega Scrafty ex darkness tank | 39.0% | **54.0%** |
| Hop's Snorlax stacked buff | 44.5% | **57.6%** |
| Steven's Carbink damage wall | 34.0% | **45.6%** |
| Decidueye ex / Judge | 35.5% | **44.8%** |
| Mega Chandelure ex retreat tax | 40.5% | **61.6%** |

Two caveats on those. `Master Ball` and `N's PP Up` have no modeled effect
in the baseline sim, and **the AI does not steer the Prize count**, so
Victory Symbol essentially never fires in simulation — it takes the sixth
Prize instead. The win rates therefore measure the damage plan only.

## Where this deck loses

- **Zoroark ex is 2 Prizes**, and the deck has no other real attacker.
  Three Knock Outs on it ends the game. 280 HP is good, not safe.
- **Weakness.** Zoroark ex is Darkness — Fighting hits it for double.
- **The Bench is the deck.** Night Joker with an empty or wrong Bench does
  nothing at all; a bench-snipe deck that removes Reshiram is removing
  your damage. Keep a second copy down.
- **Rampaging Thunder's self-lock** means the 250 mode is really 125 a
  turn. Borrow `Virtuous Flame` unless the 250 actually Knocks something
  Out.
- **Ability lock** (`Team Rocket's Watchtower` does not hit it — Zoroark ex
  is Darkness, not Colorless — but a real ability lock does) turns off
  Trade and the deck's draw collapses to its Supporters.

## Simulator work this deck required

Six fixes, four of them general rather than deck-specific:

1. **Copying a Benched Pokémon's attack was unmodeled.** Only "use the
   Defending Pokémon's attack" and Persian ex's deck-reveal shape were
   handled, so Night Joker — an entire archetype's only attack — scored 0.
2. **There was no "you win this game" mechanic at all.** Adds
   `Op.WIN_GAME`, an `own_prizes_equal` condition, and a check in
   `do_attack` that resolves before damage. It follows the copy, since
   Victory Symbol is only ever reached through Night Joker.
3. **Self-attack-lock was ignored** — *"during your next turn, this Pokémon
   can't attack"*. The AI re-used a 250-damage every-other-turn attack
   every single turn. Now tracked per Pokémon, and the drawback follows a
   borrowed copy.
4. **Borrowed attacks were ranked on raw damage**, so the AI always took
   the self-locking 250 over an unconditional 170 and attacked half as
   often. Now ranked on damage *per turn*.
5. **Energy was fed to Pokémon that could never pay their attacks.**
   `energy_shortfall` counted every printed attack, so a mono-Darkness
   deck poured Energy into a Bench Pokémon whose attack costs Fire —
   starving the one Pokémon that attacks. It now considers only attacks
   the deck's own Energy types could ever pay, and the Bench target is
   chosen by what it would hit for rather than list order.
6. **Promotion after a Knock Out picked the biggest body**, not the one
   that could fight. Now ranks on ready damage first.

Plus a minimal Stadium model: `RETREAT_STADIUMS` honours the Stadiums
whose whole effect is Retreat Cost (`N's Castle`, `Paradise Resort`),
since `Player.stadium` was previously assigned and never read. Every other
Stadium is still inert in `simulate_versus.py`.
