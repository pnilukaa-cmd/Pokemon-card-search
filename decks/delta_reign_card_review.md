# Delta Reign: every card, classified and checked

Delta Reign (set `me6`, code DLR, 141 cards) adds **99 new records** to the
pool: 88 Pokémon and 11 Trainers. The rest are alternate arts of these, plus
five reprints of older cards (Emcee's Hype, Pokémon Catcher, Growing Grass,
Bubbly Water and Nitro Fire Energy).

This page covers two things:

1. Whether each card does in the simulator what its text says.
2. Whether any of them improve the decks in the field. See
   [Are they worth adding?](#are-they-worth-adding) below.

## How each card was checked

- **Compiled:** every Ability, attack and Trainer text through the rules
  compiler, read against the card.
- **Priced:** every attack on one staged board (`dmg_check.py`), flagging
  any damage that no rule read. The board: the attacker with its own Energy;
  their Dragapult ex Active with 50 damage; a Bench of three, two with
  Abilities, one damaged; Fire Energy in my discard; six cards in their hand;
  three Pokémon of different types in mine.
- **Run:** every non-damage effect through the engine on a staged board
  (`probe.py`): where the Energy went, what was searched, what was shuffled
  back.

## What did not work, and is fixed

Each fix has a test in `test_ability_engine.py` that fails on the commit
before it.

| Card | What it did | Now |
|---|---|---|
| Darkrai (Shadow-Clad), Raikou ex (Thunder-Clad) | "Attach it to this Pokémon" went to whichever of your Pokémon the pilot ranked neediest. Shadow-Clad put both Darkness on the Bench. | On the attacker. The same fix covers 12 older cards: Okidogi ex, Zacian ex, Yanmega ex, Solgaleo, Cresselia, Deoxys, Heliolisk, Articuno, Bewear, Exeggcute, Quilladin and Thundurus (BLK). "To 1 of your Pokémon" (Misty's Vitality, Flareon ex, the Ogerpon, Energy Coin) now puts all its Energy on one Pokémon, as written. |
| Azurill (Bouncy-Bounce Charge) | "To 1 of your Benched Pokémon" could go to the Active. Smoochum's Delightful Kiss was the same. | A Benched Pokémon. |
| Mega Rayquaza Cap (Delta Gift) | One Energy in all. | One Basic Energy to each Pokémon holding a Cap. Mega Gardevoir ex's Overflowing Wishes was the same and is fixed too. |
| Tornadus, Thundurus, Landorus, Enamorus (Incarnate Solidarity) | Ignored Colorless costs with none of the other three in play. | Only with all four in play. |
| Mega Golurk ex (Restricted Activation) | Could never attack: "unless you have 10 or more cards in your hand" was dropped. | Attacks with 10+ cards in hand. |
| Raikou ex (Thunder-Clad) | Barred on the first turn like any attack. | Usable on turn 1 going first; Power Rush stays barred. |
| Magmortar (Buddy Boost) | One Fire Energy to any Pokémon. | A Basic Fire, a Basic Lightning, or one of each, from hand, to Electivire or Magmortar only. |
| Zinnia's Trust | Moved an Energy off the Active onto a Benched Pokémon, then switched in whichever Pokémon ranked best. | Switch, then one Energy from the Pokémon that went to the Bench onto the new Active. |
| Delibird (Energizing Present) | Took the top card, whatever it was. | An Energy from the top 6; the rest go to the bottom. |
| Heat Rotom ex (Rewarm) | Counted every Energy in the discard (a Lightning too), and nothing went back. | Basic Fire Energy only, then shuffled into the deck. Kyogre's Riptide and N's Darmanitan's Back Draft were the same. |
| Giratina (Chaos Crawler) | Usable every turn. | Not the turn after one of your Pokémon used it. Sylveon ex's Angelite has the same rule and is fixed too. |
| Meowscarada ex (Magical Bullet) | The 120 snipe hit an undamaged Benched Pokémon. | Damaged Benched Pokémon only. |
| Mega Rayquaza ex (Storm Emerald) | Counted only the Fire Energy. | Fire and Lightning. |
| Cacturne (Punishing Needles) | +50 for every opposing Pokémon. | Only those with an Ability. |
| Kecleon (Colorful Whip) | 30, whatever the hand held. | 30 for each type among the Pokémon in hand. |
| Ariados (Tormenting Poison) | The 4-counter Poison also hit for 40 on the spot. | Poison only. Mega Dragalge ex's Pernicious Poison hit for 160 the same way. |
| Colress's Tenacity, Adventure Lantern | Found only the first of their two cards. | Both cards. |
| Adventure Lantern | pokemontcg.io lists it as a Pokémon Tool, so it was attached and never used. | An Item, as TCGdex lists it and as its text reads. `fetch_pokemon_cards.py` now carries a `DATA_FIXES` table so a re-fetch keeps the fix. |

**Not modelled:** the Mega Rayquaza Cap's second rules line, "Mega
Evolution ex Rule: When your Mega Evolution Pokémon ex is Knocked Out, your
opponent takes 3 Prize cards." Neither API's text says the holder becomes a
Mega Evolution Pokémon ex, so a Cap holder gives up its normal Prizes here.
If the holder does count as one, every Cap holder is a three-Prize Pokémon,
and that would decide whether the card is playable.

**The pilot does not build toward Mega Golurk ex's 10 cards.** The gate is
right, but nothing holds cards back to reach 10.

## The cards

Engine column: **ok** means its text resolves as written; **fixed** means it
was fixed in the review above.

### Grass

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Heracross | Basic 130 | Attacker: High Horsepower 130 (GGC, 30 to itself); Spike Draw draws 2 | ok |
| Surskit → Masquerain | Basic 50 → Stage 1 110 | Bug Out attacker: 50 per Bug Out Pokémon in the bottom 7, for one Grass | ok |
| Cacnea → Cacturne | Basic 70 → Stage 1 130 | Attacker: Punishing Needles 10 + 50 per opposing Pokémon with an Ability; Linear Attack snipes 30 | fixed |
| Combee → Vespiquen | Basic 50 → Stage 1 120 | Combee is Bug Out ammo; Vespiquen's Clean Hit is 80 + 80 against an Evolution | ok |
| Shaymin | Basic 80 | Tech: Overrun 20 + 20 to the Bench | ok |
| Virizion | Basic 120 | Attacker: Solar Beam 110; Double Draw | ok |
| Wimpod → Mega Golisopod ex | Basic 70 → Mega 340 | Attacker: Finishing Blow 60 + 160 against a damaged Active; Quadruple Hold 160 and no retreat. Wimpod has no Retreat Cost while they have an ex in play | ok |
| Sprigatito → Floragato → Meowscarada ex | Stage 2 ex 320 | Attacker: Magical Bullet 120 + 120 to a damaged Benched Pokémon | fixed |
| Smoliv → Dolliv → Arboliva | Stage 2 150 | Disruption: Slippery Oil makes them switch their Active every turn; Mega Drain 100, heal 30 | ok |

### Fire

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Growlithe → Arcanine | Stage 1 150 | Attacker: Fervent Fang 90 + 90 at 4 Prizes or fewer; Heat Tackle 200 | ok |
| Magmar → Magmortar | Stage 1 140 | Energy engine for Electivire / Magmortar (Buddy Boost); Magmar's Gather Strength finds 2 Basic Energy | fixed |
| Torkoal | Basic 130 | Attacker: Combustion Blast 120 every other turn; Searing Flame burns | ok |
| Heat Rotom ex | Basic ex 190 | Attacker: Rewarm 30 per Basic Fire Energy in the discard, recycling them; Strong Flare 170 | fixed |
| Heatmor | Basic 110 | Tech: Destructive Flame 30, a heads discards an Energy | ok |

### Water

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Mantine | Basic 110 | Disruption: Make Waves, each player shuffles their hand and draws 4 | ok |
| Kyogre | Basic 150 | Legendary payoff: Brutal Whirlpool 100, and 50 to each of their Benched Pokémon with a Legendary Stadium in play | ok |
| Frillish → Jellicent | Stage 1 120 | Engine: Deep Sea Draw draws 1 and may put a card on the bottom (Bug Out's stacker) | ok |
| Wishiwashi ex | Basic ex 260 | Attacker / tank: Hydro Splash 220 (WWWC); Oceanic Gain heals 50 while Active | ok |

### Lightning

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Electabuzz → Electivire | Stage 1 140 | Electabuzz: Call for Family benches 2 Basics. Electivire: Voltaic Hammer 60 per Basic Energy it discards | ok |
| Eevee → Jolteon | Stage 1 110 | Attacker: Thunderbolt 220 (LLL), discarding all its Energy | ok |
| Raikou ex | Basic ex 200 | Attacker: Thunder-Clad fetches an Energy on turn 1; Power Rush 200, tails it rests a turn | fixed |
| Rotom | Basic 80 | Tech: Thunder Shock 50, may paralyse | ok |
| Thundurus | Basic 120 | Incarnate four: Thunderous Edge 90 through effects on their Active | fixed |
| Pincurchin | Basic 80 | Attacker: 20 per Energy on all their Pokémon | ok |
| Pawmi → Pawmo → Pawmot | Stage 2 150 | Energy engine: Generator's Touch attaches a Lightning from the discard each turn | ok |
| Wattrel → Kilowattrel | Stage 1 120 | Attacker: Raid 30 + 90 on the turn it evolves | ok |
| Miraidon | Basic 120 | Attacker: Flashing Bolt 120 every other turn | ok |

### Psychic

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Drowzee → Hypno | Stage 1 120 | Attacker: Mind Ruler 20 per card in their hand | ok |
| Giratina | Basic 130 | Wall attacker: Chaos Crawler 120 and no damage from attacks next turn, every other turn | fixed |
| Golett → Mega Golurk ex | Mega 350 | Attacker: Goliath's Punch 300 for PP, only with 10+ cards in hand | fixed |
| Enamorus | Basic 120 | Incarnate four: Rising Heart 100 + 100 against an ex | fixed |

### Fighting

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Sandshrew → Sandslash | Stage 1 110 | Counterattack Quills: 3 counters on any attacker that hits it while Active | ok |
| Onix → Steelix | Stage 1 190 | Tank: 60 less damage at full HP; Tough Swing 150 through Resistance | ok |
| Groudon | Basic 150 | Legendary payoff: Brutal Lands 100 + 170 with a Legendary Stadium in play | ok |
| Landorus | Basic 130 | Incarnate four: Gaia Crush 110, discards a Stadium | fixed |

### Darkness

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Nidoran♀ → Nidorina → Nidoqueen | Stage 2 170 | Maternal Call: a heads gusts every turn; Giga Impact 150 | ok |
| Spinarak → Ariados | Stage 1 100 | Spinarak is Bug Out ammo. Ariados: Tormenting Poison (4 counters a Checkup); Stealthy Sting 80, immune to Basics next turn | fixed |
| Sableye | Basic 80 | Tech: Ominous Eyes, 5 counters anywhere; Lure Out benches their Basics | ok |
| Carvanha → Sharpedo | Stage 1 120 | Crunch 60, a heads discards an Energy | ok |
| Darkrai | Basic 120 | Attacker: Shadow-Clad attaches 2 Darkness to itself; Dark Cutter 110 | fixed |
| Purrloin → Liepard | Stage 1 110 | Attacker: Follow-Up Claw 20 per damage counter on their Active | ok |
| Zorua → Zoroark ex | Stage 1 ex 270 | Attacker: Slashing Strike 210 every other turn; Riotous Beating 20 per Pokémon you have in play | ok |
| Inkay → Mega Malamar ex | Mega 320 | Attacker: Psychic Marionette 70 per Benched Pokémon they have; Eerie Wave 200, confuses | ok |
| Morpeko | Basic 80 | Setup: Call for Family benches 2 Basics | ok |
| Zarude | Basic 130 | Deadly Whip 50, 200 on two heads | ok |

### Dragon

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Druddigon | Basic 120 | Gust attack: Drag Off brings up a Benched Pokémon and hits it for 40 | ok |
| Jangmo-o → Hakamo-o → Kommo-o | Stage 2 160 | Engine: Beat Scales attaches Basic Energy from the top 6 to Dragons; Hammer In 170 | ok |
| Cyclizar | Basic 120 | Break Through 110 + 30 to the Bench | ok |

### Colorless

| Card | Stage, HP | Role | Engine |
|---|---|---|---|
| Tauros | Basic 130 | Raging Horns 50 + 10 per damage counter on itself | ok |
| Eevee | Basic 70 | Jolteon's Basic | ok |
| Delibird | Basic 90 | Energizing Present: an Energy from the top 6 while Active | fixed |
| Azurill | Basic 30 | Bouncy-Bounce Charge (free): an Energy from the deck onto a Benched Pokémon | fixed |
| Swablu → Altaria | Stage 1 110 | Cottony Carrier: your Basic Pokémon have no Retreat Cost | ok |
| Kecleon | Basic 90 | Colorful Whip: 30 per type of Pokémon revealed from hand | fixed |
| Mega Rayquaza ex | Basic Mega 280 | Attacker: Storm Emerald 50 per Fire and Lightning Energy on your board; Ruler's Roar attaches from the top 4 when benched | fixed |
| Tornadus | Basic 110 | Incarnate four: Corkscrew Dive 70, draw to 6 | fixed |
| Fletchling → Fletchinder → Talonflame ex | Stage 2 ex 280 | Talon Hunt 150 and search 2. Excited Dive puts it from hand onto the Bench while you have a Colorless Mega in play | ok |

### Trainers

| Card | Kind | Role | Engine |
|---|---|---|---|
| Aarune | Supporter | Search: up to 3 Supporters and Stadiums in any combination | ok |
| Zinnia's Trust | Supporter | Switch, and move an Energy to the new Active | fixed |
| Grisham | Supporter | Heal 50 from every Pokémon, both sides | ok |
| Tate & Liza's Training | Supporter | Draw 2; back to hand with a Legendary Stadium in play | ok |
| Tasty Rice Ball | Item | Heal 30 from the Active, +30 per Tasty Rice Ball in the discard | ok |
| Adventure Lantern | Item | Search a Basic Fire and a Basic Lightning Energy | fixed |
| Custom Vest | Tool | 60 less damage from Mega Evolution Pokémon ex (holder not a Mega) | ok |
| Mega Rayquaza Cap | Tool | Lends Delta Gift: a Basic Energy onto each Cap holder | fixed (Mega ex rule not modelled) |
| Legendary Pyroduct | Stadium | Evolution Pokémon have no Abilities, both sides | ok |
| Legendary Summit | Stadium | A Colorless Pokémon Knocked Out by an attack gives up 1 fewer Prize | ok |
| Legendary Trench | Stadium | Every heal is doubled, both sides | ok |

**By role:**

- **Energy engines:** Magmortar, Pawmot, Kommo-o, Mega Rayquaza ex,
  Darkrai, Raikou ex, Azurill, Delibird, the Cap.
- **Disruption:** Arboliva, Mantine, Nidoqueen, Druddigon, Sableye,
  Legendary Pyroduct.
- **Walls:** Giratina, Steelix, Custom Vest, Legendary Trench, Grisham.
- **Search:** Aarune, Electabuzz / Morpeko, Talonflame ex.
- **Legendary Stadium payoffs:** Kyogre, Groudon, Tate & Liza's Training.

## Are they worth adding?

**Mostly no.** Four field decks get better with a Delta Reign card, two of
them clearly. Of the 108 decks, no other one has a new card that beats a
Basic Energy in the same slot.

### How it was measured

Every field deck got the generic candidates:

- Aarune ×1.
- Custom Vest ×2.
- Legendary Pyroduct ×2, where none of the deck's own Evolution Pokémon
  has an Ability.

It also got the new attacker of each Basic Energy type it runs 8 or more
of: Darkrai, Giratina, Wishiwashi ex, Heat Rotom ex or Raikou ex. Each
candidate came with a cut fixed before any game was played (the deck's
most-played non-Boss Supporter, its Stadium or Tools, or a flex Item:
Night Stretcher, Switch, Pokégear 3.0, ...). That makes 300 variants.

1. **Panel screen:** each variant and its base list, 100 games against 16
   opponents, on the same seeds.
2. **Full field:** the 40 hits of +2 or more, 100 games against all 107
   other decks.
3. **Two controls** for the 17 that held:
   - The same cut filled with Basic Energy instead of the new card. This
     shows whether the gain was the card or just the cut.
   - The same card with a different cut.

The details and every deck's numbers are in
`runs/2026-11-12/delta_reign_field_review/README.md`.

### Worth adding

| Deck | Change | vs the list | vs Basic Energy in the slot | With a second cut |
|---|---|---|---|---|
| `feraligatr_munkidori_damage_transfer` | +2 Wishiwashi ex DLR 29, −2 Switch MEG 130 | **+4.84 ± 0.93** | +4.62 ± 0.99 | +5.38 (−2 Night Stretcher) |
| `kyurem_vanilluxe_blizzard` | +2 Wishiwashi ex DLR 29, −2 Switch MEG 130 | **+4.26 ± 0.89** | +2.60 ± 0.75 | +3.51 (−Night Stretcher, −Lillie's) |
| `munkidori_ex_pecharunt_chains` | +2 Legendary Pyroduct DLR 94, −2 Pokégear 3.0 BLK 84 | **+1.82 ± 0.79** | +2.50 ± 0.72 | +2.76 (−2 Night Stretcher) |
| `team_rocket_hypno_exeggutor` | +2 Legendary Pyroduct DLR 94, −1 Team Rocket's Factory ASC 203, −1 Night Stretcher MEG 173 | **+2.64 ± 0.72** | +1.59 ± 0.75 | +2.68 (−2 Night Stretcher) |

- **Wishiwashi ex** (Basic ex, 260 HP, Hydro Splash 220 for Water ×3 +
  Colorless, heals 50 while Active) is a big Basic body the two Water
  decks did not have. In the Feraligatr list it attacked 1.04 times a game
  and healed itself 2.11 times. It slows that deck's own setup (Croconaw
  by turn 6: 63% → 51%), and still wins more.
- **Legendary Pyroduct** (Evolution Pokémon have no Abilities, both
  sides) costs these two decks nothing of their own. It switches off
  Drakloak, Dudunsparce, Kirlia and the field's other Evolution engines.

### Positive, but not clearly better than an Energy

Legendary Pyroduct in these decks measured +1.8 to +2.5 against the list,
but only +1.0 to +1.5 (under 2 SE) over a Basic Energy in the same slot,
and less with a second cut:

- `mega_absol_ex_hand_lock`
- `mega_malamar_ex_psychic_marionette`
- `team_rocket_moltres_houndoom`
- `team_rocket_nidoking_nidoqueen`

Worth trying; not proven.

### Not worth adding

- **The gain was the cut, not the card:**
  - Darkrai in `static_venom_drapion` (+3.74) and `darkness_mill_hand_lock`
    (+3.15).
  - Legendary Pyroduct in `aggron_diggersby_angry_slam` (+3.53), the two
    Arbok / Muk decks (+1.5) and `mew_dbc_hypno` (+1.76).

  A Basic Energy in the same slot did as well or better. Those decks want
  less Switch or Night Stretcher, not the new card.
- **Aarune** (search 3 Supporters / Stadiums) in a Lillie's Determination
  slot: −1.12 on average over 107 decks, 42 of them worse by more than 1.5.
  A draw Supporter is worth more than a tutor in this field.
- **Custom Vest:** −0.38 on average over 108 decks. Its panel hits did not
  hold on the full field (Dragapult ex: −0.15; arbok_muk_trolley: −0.27).
- **Giratina** (−3.79 over 15 Psychic decks), **Heat Rotom ex** (−5.83 over
  6 Fire decks), **Darkrai** elsewhere (−0.29 over 26), **Raikou ex** (its
  one Lightning deck, −0.69).
- **Already measured in their own reviews:**
  - Legendary Trench, Tasty Rice Ball and Grisham: neutral in the
    Kangaskhan heal wall (`decks/kangaskhan_legendary_trench_wall.md`).
  - Mantine's Make Waves, Inkay's Knock Off, Sandslash's Digging Claw and
    Giratina: lost in the mill and hand-lock decks
    (`runs/2026-11-10/delta_reign_mill_cards`).
  - Legendary Summit and Tauros: strong, but only in the Maushold mill
    deck (`decks/maushold_mill_legendary_summit.md`).

**Built on Delta Reign:**

- Bug Out (Masquerain, Jellicent): 49% against the field.
- Mega Malamar ex: about 77%.
- The Maushold mill with Legendary Summit.
- The Kangaskhan wall with Legendary Trench: 85%.

Those are the sets' best uses so far, rather than additions to old decks.

### A side finding

`mega_zygarde_cinderace_turbo_flare` measured **+12.01 ± 0.70** against
the field with its Core Memory and one Pokégear 3.0 replaced by 2 Basic
Fighting Energy. Custom Vest in that slot was +9.03. Custom Vest in the
Pokégear slot, keeping Core Memory, was −0.21. So it is the Energy, or
losing Core Memory (Geobuster needs four Fighting Energy from a 12-Energy
deck), not the Vest. Which of the two was not separated here.

**Not tested:**

- Cards with no field deck to fit: the Incarnate four together, Mega
  Golurk ex, Mega Rayquaza ex with its Cap, Magmortar / Electivire.
- Tasty Rice Ball, Zinnia's Trust and Adventure Lantern as general
  additions.
