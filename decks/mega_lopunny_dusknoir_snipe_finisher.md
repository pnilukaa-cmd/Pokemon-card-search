# Mega Lopunny ex / Dusknoir — snipe and finish

Analysis of a user-supplied list, plus the three-card change that took it
from **57.1%** to **64.9%** mean win rate across the full field.

## What the deck is doing

Two halves that multiply.

**Dusknoir** SFA 20 — Ability `Cursed Blast`: *"Once during your turn, you
may put **13 damage counters** on 1 of your opponent's Pokémon. If you use
this Ability, this Pokémon is Knocked Out."*

**130 damage, anywhere on their board, for no Energy and no attack.** The
support is built for exactly this:

- `Duskull` SFA 18's `Come and Get You` puts **up to 3 Duskull from the
  discard onto your Bench** — the line rebuilds itself.
- `Lana's Aid` returns up to 3 non-Rule-Box Pokémon from discard to hand,
  which is Duskull/Dusclops/Dusknoir specifically.
- 4 `Rare Candy` skips Dusclops entirely: Duskull → Dusknoir.

**Mega Lopunny ex** PFL 84 (Stage 1 MEGA ex from Buneary, 330 HP) —
`Gale Thrust`: `Colorless`, 60+, ***"If this Pokémon moved from your Bench
to the Active Spot this turn, this attack does 170 more damage."***

**230 damage for one Energy**, on the turn you `Switch` it in. That is why
there are 4 Switch.

Put together: `Cursed Blast` for 130 → `Boss's Orders` → `Switch` →
`Gale Thrust` for 230 = **360 damage** on a target of your choosing.
Nothing in the format survives that, and it costs one Energy.

`Spiky Hopper` (`CC`, 160) is the backup: *"damage isn't affected by any
effects on your opponent's Active"* — it goes through `Steven's Carbink`,
`Granite Cave`, and every other −30 wall.

## Set numbers

All 11 unresolved lines check out. `Mega Lopunny ex PFL 84` (PFL 83 is
Buneary, and 84 is the gap right after it), `Bronzor TEF 68` (between
Latias 67 and Bronzong 69 — and correctly the *Psychic* Bronzor matching
the Psychic Bronzong), `Meowth ex POR 62`, `Poké Pad POR 81` (between
Poké Ball 80 and Pokémon Catcher 82), `Hilda WHT 84`, `Latias ex SSP 76`,
`Dusclops PRE 36`, `Dawn PFL 129` (PFL runs to 130), `Night Stretcher
ASC 196`. Nothing to correct.

`check_energy_support.py` flags 8 Metal costs as IMPOSSIBLE — **all false
positives**. It pools every printing sharing a name, and the Bronzor and
Bronzong being run are the Psychic TEF pair (`Mirror Attack` P,
`Evolution Jammer` P), which the Psychic line pays for fine.

## The problem: five Energy

1000-trial baseline on the list as sent: **first attack landed by turn 6
in only 67.9% of games.** For comparison, other decks in this folder sit
at 87–91%. One game in three, the deck never attacks at all.

Five Energy is not enough even for a deck whose main attack costs one,
because `Gale Thrust` needs an Energy on Lopunny *specifically*, Lopunny
is 330 HP and 3 Prizes so it does get Knocked Out, and re-arming needs
another. `Telepathic Psychic Energy`'s Bench-search only triggers when
attached to a **Psychic** Pokémon — Mega Lopunny ex is **Colorless**, so
every copy sent to the attacker is a blank search.

## The three cards to cut

**Flutter Mane, Latias ex, Meowth ex** — three singletons, each arriving
in ~28% of games by turn 6, in a deck with no room for them.

`Latias ex` deserves a specific note: `Skyliner` gives your **Basic**
Pokémon no Retreat Cost. **Mega Lopunny ex is a Stage 1**, so Skyliner
does *not* enable `Gale Thrust` — the card that looks like it turns on the
combo does not. `Switch` is what moves Lopunny from Bench to Active, and
switching is not retreating, so the Retreat Cost was never the obstacle.

That is a genuine 2-Prize liability doing nothing for the main plan.

```
-1 Flutter Mane TEF 78     +3 Basic Psychic Energy
-1 Latias ex SSP 76        +1 Buneary PFL 83
-1 Meowth ex POR 62        -1 Hilda WHT 84
```

Which tested markedly better than the alternative way of finding the same
three slots — cutting a `Switch`, a `Poké Pad` and a `Hilda` instead only
reached 59.7% mean, because those three are load-bearing:

| Build | first attack by T6 | mean win rate | winning matchups |
| --- | --- | --- | --- |
| as sent (5 Energy) | 67.9% | 57.1% | 19/27 |
| +3 Energy, cutting Switch/Poké Pad/Hilda | 76.3% | 59.7% | 21/27 |
| **+3 Energy, cutting the three singletons** | **85.1%** | **64.9%** | **24/27** |

Mulligan does move the wrong way — 13 Basics (16.3%) down to 11 (22.2%) —
which is why the 4th Buneary goes back in rather than a 4th Trainer. It is
a real cost, and it is worth paying for an 17-point swing in whether the
deck attacks at all.

## Revised list

```
Pokémon: 22
4 Buneary PFL 83
3 Mega Lopunny ex PFL 84
2 Bronzor TEF 68
2 Bronzong TEF 69
4 Duskull SFA 18
2 Dusclops PRE 36
4 Dusknoir SFA 20
1 Budew ASC 16

Trainer: 30
4 Lillie's Determination MEG 119
3 Hilda WHT 84
2 Lana's Aid TWM 155
1 Dawn PFL 129
2 Boss's Orders MEG 114
4 Poké Pad POR 81
4 Rare Candy MEG 125
1 Night Stretcher ASC 196
4 Switch MEG 130
4 Ultra Ball MEG 131
1 Nighttime Mine ASC 197

Energy: 8
4 Telepathic Psychic Energy POR 88
3 Basic Psychic Energy
1 Enriching Energy SSP 191

Total Cards: 60
```

## Numbers

Full field, 200 games per matchup — mean **64.9%**, median **64.5%**,
**24/27** winning:

| Win rate | Opponent | | Win rate | Opponent |
| --- | --- | --- | --- | --- |
| **84.5%** | Feraligatr / Munkidori | | 64.5% | Water aggro |
| **83.0%** | Eerie Inferno Ninetales | | 63.5% | Arbok / Muk (Trolley) |
| **78.5%** | T.R. Wobbuffet / Orbeetle | | 63.5% | T.R. Crobat / Mega Absol |
| **78.5%** | Salazzle ex / T.R. Muk | | 62.5% | Krookodile ex / Relicanth |
| **76.0%** | Darkness mill hand lock | | 59.0% | Toxic Slumber Vileplume ex |
| **74.0%** | Chandelure / Centiskorch | | 59.0% | Panic Poison Paralysis |
| **74.0%** | Arbok / Muk (Laser) | | 58.5% | T.R. Persian ex |
| **71.5%** | T.R. Spidops swarm | | 58.0% | Mega Scrafty ex |
| **71.5%** | Hop's Snorlax | | 56.0% | Steven's Carbink wall |
| **68.5%** | Static Venom Drapion | | 56.0% | Decidueye ex / Judge |
| **67.5%** | Arbok / T.R. Muk | | 48.5% | N's Zoroark ex Night Joker |
| **65.5%** | Orthworm ex metal | | 45.5% | Mega Chandelure ex retreat tax |
| **65.0%** | T.R. Koffing / Weezing | | **40.0%** | **Lurantis heal punish** |

`selective_bloom_cradily` excluded — zero Basic Pokémon the engine can put
into play, so it mulligans out.

## Where it loses

- **Healing (40.0% vs Lurantis).** `Cursed Blast` is a one-shot that costs
  you a Prize; anything that heals the 130 off undoes the whole
  investment. This is the deck's worst matchup by a clear margin.
- **The Prize economy is the real constraint.** Every `Cursed Blast` hands
  the opponent a Prize (Dusknoir is not an ex). Four activations is four
  of the six Prizes they need — so 130 damage has to convert into a Knock
  Out nearly every time, not be sprinkled. And a Knocked Out Mega Lopunny
  ex gives up **3** on its own.
- **Retreat-tax decks** (Mega Chandelure ex, 45.5%). `Gale Thrust`'s bonus
  needs Lopunny to *move from Bench to Active*; a Binding Flame board plus
  a dead Switch turns a 230-damage attack into a 60.
- **Dusknoir is a Stage 2 on 4 Rare Candy**, and Rare Candy cannot be used
  on a Basic put into play that same turn — so the fastest possible
  Dusknoir is turn 2 at the earliest, and lands turn 3.81 on average.
