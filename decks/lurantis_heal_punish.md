# Lurantis ex Heal-Punish

**The question this deck answers**: can you build a deck that just out-heals the meta?

Short answer, honestly: **no, not as pure stall.** Prize cards are the actual win condition
in Standard, not attrition, and a couple of our own past decks in this repo already show why
pure walling fails — the [Feraligatr/Munkidori build](feraligatr_munkidori_damage_transfer.md)
puts up 280-310 damage in a single hit for 2 Energy, which one-shots *any* Pokémon in this
pool, healing or not. No amount of "heal 30 a turn" survives a 300-damage swing.

The real answer is to stop treating healing as pure defense and use it as **fuel for offense**
instead. Scanning every healing ability/attack/Trainer in the Standard pool (30+ healing
abilities, 60+ healing attacks, 15+ healing Trainers) turned up a specific sub-family of Grass
attacks that only unlock their real damage *if the user was healed that turn*:

| Card | Attack | Base | If healed this turn |
|---|---|---|---|
| **Lurantis ex** | Lively Cutter | 60 | **+200 → 260 damage**, for 1 Grass Energy |
| Vileplume | Lively Flower | 60 | +120 → 180 damage |
| Maractus | Lively Needles | 20 | +100 → 120 damage |

Lurantis ex is the standout: 260 HP, only Stage 1 (no Rare Candy needed), retreat cost 1, and
its payoff attack costs a single Grass Energy. That's a 1-energy, 260-damage attack — enough
to one-shot almost anything in the format, including the 280-HP Feraligatr from the deck
above — contingent entirely on healing being part of your turn.

## The loop

1. Opponent attacks your Active Lurantis ex, putting damage counters on it (this is required —
   standard Pokémon TCG rules only count a Pokémon as "healed" if a damage counter was
   actually removed from it, so Lurantis needs to have taken a hit first).
2. On your turn, play any cheap healing Item (`Potion`, `Arven's Sandwich`, `Lumiose Galette`)
   on Lurantis ex, or trigger `Erika's Vileplume ex`'s free repeatable Ability. Items have no
   "once per turn" limit, so this is reliable, not a coin flip.
3. Attack with `Lively Cutter` for 260 damage — the opponent's own attack just got turned
   into your biggest hit of the game.
4. Optionally `Boss's Orders` first to gust up a wounded Bench target instead, guaranteeing
   a clean KO on whatever's weakest.

In effect, the harder the meta hits you, the harder you hit back — which is about as close
to "out-healing" a hyper-aggro format as is actually achievable within the prize-card ruleset.

## Centerpieces

1. **Lurantis ex** (Paldean Fates equivalent print, Stage 1 from Fomantis) — 260 HP, the
   payoff attacker described above. Weak to Fire (×2) — this is the deck's one real
   vulnerability, discussed below.

2. **Erika's Vileplume ex** (Stage 2 from Erika's Oddish → Erika's Gloom) — 310 HP wall.
   Ability `Lovely Fragrance`: once per turn, heal 30 from *each* of your Pokémon, for free,
   no discard, no card cost. This is the most reliable enabler in the deck since it doesn't
   compete with the Supporter-for-turn slot the way `Cook`/`Pokémon Center Lady` would.
   Slow to set up (full Stage 2 line), so it's a 1-of-1-of-1 backup engine, not the primary plan.

3. **Maractus** (Basic, no evolution needed) — 100 HP, `Lively Needles` for 20(+100 if
   healed) off a single Grass Energy. Fills the early game before Lurantis ex is online with
   the same heal-payoff shape, so early Potions aren't wasted turns.

## Decklist (60 cards)

### Pokémon (14)

| Qty | Card | Set | Role |
|---|---|---|---|
| 4 | Fomantis | Paldean Fates (PBL 3) | Feeds Lurantis ex |
| 4 | Lurantis ex | Paldean Fates (PBL 4) | Centerpiece payoff attacker |
| 3 | Maractus | Black Bolt (BLK 8) | Early heal-payoff attacker |
| 1 | Erika's Oddish | Ascended Heroes (ASC 1) | Feeds Erika's Vileplume ex |
| 1 | Erika's Gloom | Ascended Heroes (ASC 2) | Bridge (skip with Rare Candy) |
| 1 | Erika's Vileplume ex | Ascended Heroes (ASC 3) | Free repeatable team heal + 310 HP wall |

### Trainers (31)

| Qty | Card | Type | Effect |
|---|---|---|---|
| 4 | Potion | Item | Heal 30, no downside — primary enabler |
| 3 | Arven's Sandwich | Item | Heal 30 from Active, no downside |
| 2 | Lumiose Galette | Item | Heal 20 + cure Special Condition |
| 1 | Poké Vital A | ACE SPEC | Heal 150 — emergency save + guaranteed enable |
| 4 | Ultra Ball | Item | Discard 2, search any Pokémon |
| 4 | Buddy-Buddy Poffin | Item | Bench 2 Basics ≤70 HP (Fomantis, Erika's Oddish) |
| 2 | Rare Candy | Item | Skip Erika's Gloom straight to Erika's Vileplume ex |
| 3 | Boss's Orders | Supporter | Gust the weakest target for the Lively Cutter KO |
| 2 | Drayton | Supporter | Search a Pokémon + a Trainer |
| 2 | Lillie's Determination | Supporter | Shuffle hand, draw 6 (8 late-game) |
| 2 | Night Stretcher | Item | Recur a KO'd Pokémon or Basic Energy |
| 2 | Switch | Item | Retreat utility |

### Energy (15)

| Qty | Card |
|---|---|
| 15 | Basic Grass Energy |

Mono-Grass works throughout — every payoff attack costs Grass or Grass+Colorless, and
Colorless is payable by any Basic Energy.

## Design notes / weaknesses

- **Fire is a hard counter.** Every Pokémon in this list (Fomantis, Lurantis ex, Maractus,
  the Erika's line) is Weak to Fire ×2, which is standard for Grass-type Pokémon. Against a
  Fire matchup, incoming damage doubles, which both threatens to one-shot Lurantis ex before
  it can heal-and-swing and makes the healing math worse across the board. No tech slot is
  reserved for this — it's the honest cost of leaning fully into one type's heal-payoff theme.
- **The "healed this turn" condition needs prior damage.** Lurantis ex can't just proactively
  self-heal for value on a full-HP board — it needs to have actually taken a hit first. This
  makes the deck naturally reactive: it's strongest specifically *against* aggressive decks
  that attack early and often, which is exactly the matchup "out-heal the meta" is aimed at.
- 14 Pokémon / 31 Trainer / 15 Energy, 8 Basics, verified to parse to exactly 60 cards and
  clean (0 recommendations flagged) through the app's own recommendation engine.

## Pokémon TCG Live Import

```
Pokémon: 14
4 Fomantis PBL 3
4 Lurantis ex PBL 4
3 Maractus BLK 8
1 Erika's Oddish ASC 1
1 Erika's Gloom ASC 2
1 Erika's Vileplume ex ASC 3

Trainer: 31
4 Potion POR 83
3 Arven's Sandwich DRI 161
2 Lumiose Galette POR 78
1 Poké Vital A SFA 62
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin TEF 144
2 Rare Candy MEG 125
3 Boss's Orders MEG 114
2 Drayton SSP 174
2 Lillie's Determination MEG 119
2 Night Stretcher SFA 61
2 Switch MEG 130

Energy: 15
15 Basic Grass Energy

Total Cards: 60
```
