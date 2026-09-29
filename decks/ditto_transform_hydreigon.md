# Ditto Transform: Hydreigon ex / Tyranitar / Gengar ex

<!-- field-results -->
> ### Field results — 2026-09-29
> **69.8% mean · 71.0% median · 50 of 56 winning matchups · rank 3 of 57**
>
> Best `team_rockets_wobbuffet_orbeetle_damage_launder` 95% · worst `team_rockets_persian_ex_attack_theft` 34%.
>
> Full round robin, 1000 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates 2026-09-29** and was measured against a different field or engine.
<!-- field-results -->


Built 2026-09-28 from the request "get Ditto early and swap it for big
Stage 2s, or ones with hard-to-handle early effects (Tyranitar's Item
lock)". Ditto 30C 115's Surprisingly Transform puts any Pokemon from the
deck into play with Ditto's Energy still attached, so a Stage 2 arrives on
turn 1 going second, with no Stage 1 and no Rare Candy.

**69.76% against the 55-deck field, 1000 games per opponent, winning 49
of 54; +4.25 ± 0.89 over the original Ditto list on the same dice.**
Worst: Team Rocket's Persian ex 32.7, Lurantis heal-punish 35.2, N's
Zoroark toolbox 39.0.

## 2026-09-29: Hero's Cape for Secret Box (+2.75)

Built for an UNKNOWN field, so the target was the deck's weak spots
rather than any one opponent. Its three worst matchups (Team Rocket's
Persian ex 34, Lurantis 37, N's Zoroark 40) share a cause: Grass attackers
(Spidops, Lurantis) hit Hydreigon ex for double, so 180 becomes 360 and
takes a 330 HP body in one swing. Hero's Cape (the ACE SPEC slot, +100 HP)
makes it 430. **Paired, 1000 games x 54 opponents: +2.75 +/- 0.36, 70.25 ->
73.00%** -- level with the field's best. The gain is broad (the floor
barely moves): a bigger Ditto/Hydreigon survives a hit it did not before
against most of the field, not just the Grass decks.

Tried and rejected on the way (200 games, paired): Persian ex as a second
Transform target +0.27 (noise), three -0.76; Dragapult ex instead of
Hydreigon (no Weakness) -6.8 / -5.8; zero-retreat openers instead of
Farfetch'd (Larry's Dunsparce -6.8, Marnie's Morpeko -10.6); Prime Catcher
for Secret Box -0.44.

## The plan

Going second, turn 1: Poffin two Ditto, attach, Crispin attaches a
second Energy, Backtrack Badge on the Active Ditto, Transform (3 in 4 with
the Badge re-flip) into Hydreigon ex: 330 HP holding 2 Energy. Turn 2:
attach, Crashing Headbutt for 200 and mill 3. Going first, all of it is a
turn later. Tyranitar and Gengar ex are the alternate targets the pilot
picks when they hit harder (Tyranitar's Daunting Gaze stops Items while
it is Active; Gengar ex's Gnawing Curse punishes every Energy attached).
Kofu and Lillie's put stranded Stage 2s back into the deck.

Soft spots: a 25% Transform whiff leaves a 70 HP Ditto (Fighting weak)
Active; Benched Ditto are one-Prize gust targets; Hydreigon ex is Grass
weak. Obsidian (needs Psychic) is left uncastable on purpose.

## What was tested (all measured, paired)

- **Budew as an Item-lock opener** (free Itchy Pollen, then Tyranitar to
  keep the lock): 4 Budew -> 2 was +1.42, and 0 Budew with Farfetch'd as
  the extra Basic was +2.5 more. Budew's 30 HP gives Prizes away, and
  Boss's Orders onto a Benched Budew switches Tyranitar's lock off.
- **Making the Transform prefer the Item lock** (a pilot rule valuing
  Daunting Gaze): -1.22 and -3.72 at two weights, -1.06 when only early.
  Reverted. Hydreigon ex's 200 damage and 330 HP beat the lock here.
- **Slaking ex** (280 for two Colorless): measured strong until the engine
  was found ignoring Born to Slack; with the gate fixed, 0 Slaking ties 2.
- Mega Gengar ex instead of Gengar ex: -0.61 (three Prizes).
- **Other Darkness targets in the Gengar ex slot** (2026-09-28, 200 games,
  paired): Crobat CRI 51 -0.29, Marnie's Grimmsnarl ex -0.55, Gengar ex
  30C -0.47, Tyranitar ex PRE 64 +1.38 -- which at 1000 games was -0.07
  +/- 0.28 (two Tyranitar ex: +0.08 +/- 0.30). The one-of slots do not
  move the deck; Hydreigon ex does the work. Crobat, Toxtricity and
  Mandibuzz were mis-modelled until this study and are fixed.
- **Why Farfetch'd**: it is a sixth Basic that Poffin finds (70 HP),
  bought for the mulligan rate (60% -> 46%), measured +1.07 as a fifth
  Basic. Impromptu Carrier is a small bonus (it takes Air Balloon); it
  now declines a Backtrack Badge it cannot use.
- **Turn 1**: only the player going FIRST cannot attack on turn 1. Going
  second, Crispin's second Energy makes a turn-1 Transform legal.

1000-trial baseline: Ditto in play 98.2% (avg turn 1.27), first attack by
turn 6 in 97.2% (avg 2.27), Hydreigon ex by turn 6 61.6% (avg 2.87). The
baseline cannot retreat, so a Farfetch'd opener never lets Ditto attack
there; the versus numbers above retreat.

## PTCGL import

```
Pokémon: 12
4 Ditto 30C 115
2 Farfetch'd TWM 132
4 Hydreigon ex SSP 119
1 Tyranitar JTG 95
1 Gengar ex TEF 104

Trainer: 37
4 Crispin SCR 133
4 Lillie's Determination MEG 119
2 Kofu SCR 138
2 Boss's Orders MEG 114
1 Team Rocket's Petrel ASC 207
4 Buddy-Buddy Poffin MEG 167
4 Pokégear 3.0 BLK 84
4 Night Stretcher MEG 173
3 Ultra Ball MEG 131
2 Energy Switch MEG 115
1 Switch MEG 130
1 Hero's Cape TEF 152
4 Backtrack Badge PBL 74
1 Air Balloon MEG 166

Energy: 11
8 Basic Darkness Energy
3 Basic Metal Energy

Total Cards: 60
```
