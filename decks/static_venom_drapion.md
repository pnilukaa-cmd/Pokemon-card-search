# Static Venom (Skorupi / Drapion)

<!-- field-results -->
> ### Field results — 2026-09-10
> **28.7% mean · 26.8% median · 3 of 34 winning matchups · rank 33 of 35**
>
> Best `team_rockets_wobbuffet_orbeetle_damage_launder` 68% · worst `lurantis_heal_punish` 14%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the ex audit and is not comparable**: that audit corrected typed-Energy scalers that counted the wrong Energy, discard-cost attacks that were never charged, and attack gates that were never enforced.
<!-- field-results -->




Fourth of five decks built around the Special Condition stacking research in this repo (see
`combo_patterns.md` Pattern 5). A second guaranteed same-turn **Paralyzed + Poisoned** lockdown
line, mono-Darkness, kept deliberately lean (a single evolution line, no splash) rather than
adding a Fighting secondary for Glimmora — the deck's whole cost curve is already
Darkness-only, and a splash would add a second energy-type failure point for no attack this
deck actually needs.

## Centerpieces

1. **Drapion** (Phantasmal Flames) — `Hazardous Tail` (3 Darkness) does 100 damage and
   inflicts Paralyzed + Poisoned on the opponent's Active, no coin flip — but it also does 70
   damage to Drapion itself. At 140 HP, that's a two-shot-max move before self-damage alone
   threatens the KO, so it's the finisher, not the every-turn attack. `Wrack Down` (2 Darkness,
   60 damage, no downside) is the actual workhorse.

2. **Skorupi** (Phantasmal Flames) — `Poison Jab` (2 Darkness, 20 damage) independently
   inflicts Poisoned, useful chip before Drapion is online.

3. **Cook** (Supporter, heal 70 from Active) — included specifically to reset Drapion's own
   Hazardous Tail self-damage between swings.

## Design notes

- Rare Candy is deliberately absent — Drapion is only Stage 1 (evolves directly from the Basic
  Skorupi), so Rare Candy (which skips a Stage 1 en route to a Stage 2) doesn't apply to this
  line at all.
- Rescue Board (retreat cost reduction, free retreat at ≤30 HP) covers Drapion once it's sitting
  low from its own Hazardous Tail recoil.
- Prime Catcher (1x, ACE SPEC) is the deck's only non-4x trainer.
- Verified with `check_energy_support.py`: mono-Darkness supply (11 Darkness Energy) covers
  every attack cost with no shortfalls; no attack-gating Ability text found; every card name in
  the list matched `pokemon_standard_cards.json`.

## Pokémon TCG Live Import

```
Pokémon: 8
4 Skorupi POR 51
4 Drapion POR 52

Trainer: 41
4 Ultra Ball MEG 131
4 Poké Ball POR 80
4 Boss's Orders MEG 114
4 Cheren ASC 258
4 Judge POR 76
4 Switch MEG 130
4 Night Stretcher MEG 173
4 Cook TWM 147
4 Air Balloon MEG 166
4 Rescue Board TEF 159
1 Prime Catcher TEF 157

Energy: 11
11 Basic Darkness Energy

Total Cards: 60
```
