# N's Zoroark ex — Night Joker toolbox

<!-- field-results -->
> ### Field results — 2026-09-13
> **50.1% mean · 48.0% median · 18 of 43 winning matchups · rank 26 of 44**
>
> Best `static_venom_drapion` 76% · worst `arbok_muk_trolley_darkbell` 34%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->












`N's Zoroark ex` ASC 137, Stage 1, 280 HP.
**`Night Joker`, `D``D`: choose 1 of your Benched N's Pokémon's attacks
and use it as this attack.**

## The point, which is not obvious from the card

**Night Joker launders the Energy cost.** You pay `D``D` and get the
chosen attack's *effect*, not its cost. So:

| On its own card | Borrowed |
| --- | --- |
| `N's Zekrom` Rampaging Thunder — `F``L``L``C`, **250** | **`D``D`, 250** |
| `N's Reshiram` Virtuous Flame — `F``F``L``C`, **170** | **`D``D`, 170** |
| `N's Vanilluxe` Blizzard — `W``C``C`, 120 + 10 each Bench | `D``D`, same |

Zekrom and Reshiram are **Basics with four-Energy, two-type attacks that
this deck can never pay for** — and it never needs to. They sit on the
Bench as attack-holders and never attack. The deck is mono-Darkness and
throws 170 every turn.

`Rampaging Thunder` locks its user out of attacking next turn, and **the
lock follows the copy**, so 250 is an every-other-turn button.
`Virtuous Flame` at 170 with no drawback is the one you press.

## Where the damage was going missing

The previous build measured **35.9%** and the trace said why — nothing to
do with damage. Night Joker landed 170 thirty-two times in 25 games, 250
seven times, and 480 into Weakness. The damage was never the problem.

**Zoroark ex was.** Measured over 1500 openings:

| | T1 | T2 | T3 | T4 | T5 | T6 |
| --- | --- | --- | --- | --- | --- | --- |
| N's Zorua | 69.5% | 92.3% | 95.0% | 96.3% | 97.5% | 98.4% |
| **N's Zoroark ex** | 0% | **29.9%** | 45.4% | 52.7% | 58.8% | **64.3%** |

Zorua is out on turn 2 almost always; the thing that actually attacks is a
coin flip by turn 4. And the reason is a rules detail that is easy to miss:

**`Poké Pad` cannot fetch `N's Zoroark ex`** — it searches a Pokémon
*that doesn't have a Rule Box*, and Zoroark ex has one. Four copies of the
deck's main tutor could not touch its main card. `Ultra Ball` and one
`Master Ball` were the only outs.

**`Cyrano` SSP 170 — search your deck for up to 3 Pokémon ex** — is the
answer, and it takes three at once.

The second finding, from `ai_quality.py`: the deck was **idle on 37% of
its attacking turns, and 87% of those were simply no Energy in hand.**
Eleven Energy in a deck that needs `D``D` every single turn is too thin.

| change | mean | median | winning |
| --- | --- | --- | --- |
| previous build | 35.9% | 34.5% | 4/31 |
| + Cyrano, Energy 11 → 14, cut dead weight | 44.6% | 42.0% | 9/32 |
| **+ Basics 10 → 12 (mulligan 25.9% → 19.1%)** | **45.3%** | **42.2%** | **12/32** |
| *same build, independent seed* | **44.9%** | **45.2%** | **9/32** |

**+9.4 and +8.4 on two independent seeds**, paired, 200 games per matchup.

## Why `N's Vanilluxe` is not in this deck

It was tested, in two separate shells, and it earns nothing.

`Snow Coating` (`C``C`) **doubles the damage counters on each of your
opponent's Pokémon**. The maths is genuinely exciting — 20 → 40 → 80 →
160 → 320 — and the maths is the trap. **Doubling zero is zero**, and by
the time you have placed enough counters for doubling to matter, you would
rather have attacked twice.

Measured:

| build | mean | winning |
| --- | --- | --- |
| N's Zoroark + Vanilluxe + Uxie seed | 17.5% | 0/32 |
| leaner version of the same | 11.0% | 0/32 |
| Palossand ex + Vanilluxe | 35.4% | 6/32 |
| **the same deck with Vanilluxe removed entirely** | **35.3%** | **5/32** |

That last pair is the answer: **removing Vanilluxe changed nothing.**
Palossand ex was carrying the deck; Vanilluxe was a passenger. The
attack-usage trace on the first build shows why — its most-used attacks
were `Call for Family` (0 damage), `Scratch` (20), and `Painful Memories`
(0 damage). Five slots of Stage 2 line to hold a card that never attacked.

**The one place the doubling is real**, recorded because it is a genuinely
clean piece of maths: `Palossand ex`'s `Barite Jail` puts counters on each
Benched Pokémon *until its remaining HP is 100*, so a Pokémon with H HP
takes H−100. Snow Coating doubles that to 2(H−100), which is lethal
whenever **H ≥ 200** — every ex and Mega ex on their Bench, in two
attacks. It still measured at 35%, because assembling a Stage 1 ex and a
Stage 2 across three Energy types costs more than the wipe returns.

## Decklist

```
Pokémon: 17
4 N's Zorua ASC 136
4 N's Zoroark ex ASC 137
4 N's Reshiram ASC 154
2 N's Zekrom ASC 155
2 N's Purrloin JTG 96
1 N's Darmanitan ASC 33

Trainer: 29
4 Buddy-Buddy Poffin MEG 167
4 Ultra Ball MEG 131
3 Cyrano SSP 170
3 Boss's Orders MEG 114
3 Lillie's Determination MEG 119
2 Poké Pad ASC 198
2 Xerosic's Machinations SFA 64
2 N's Castle JTG 152
2 N's PP Up ASC 195
2 Night Stretcher MEG 173
1 Energy Search POR 72
1 Master Ball TEF 153

Energy: 14
14 Basic Darkness Energy

Total Cards: 60
```

- **`N's Castle` gives every N's Pokémon no Retreat Cost** — including
  your opponent's, if they run them. It is what lets the toolbox rotate.
- **`Buddy-Buddy Poffin` reaches Zorua (70), Purrloin (70) and Joltik**
  but **not** Reshiram or Zekrom at 130. The big attack-holders come from
  Ultra Ball and Poké Pad, which *can* fetch them — they have no Rule Box.
- **`Xerosic's Machinations`** puts their hand to 3. It has **no modeled
  effect in the simulator**, so its disruption is not counted in the
  figure below.

## Numbers

60 cards, no card over 4, one ACE SPEC, mulligan **19.1%** (12 Basics).
One UNCASTABLE flag: `N's Reshiram`'s *secondary* attack Powerful Rage
needs Fire — irrelevant, because Reshiram never attacks from its own card.
That flag is the deck working as designed.

Full field, 32 decks, 200 games each, paired — mean **45.3%**, median
**42.2%**, **12/32** winning.

It is still a below-average deck in this field, and the remaining ceiling
is structural: **every body that matters is a 2-Prize ex throwing 170**,
so it needs four Knock Outs to their three.
