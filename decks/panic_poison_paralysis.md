# Panic Poison (Ekans/Arbok + Team Rocket's Muk)

<!-- field-results -->
> ### Field results — 2026-09-10
> **73.8% mean · 73.0% median · 36 of 37 winning matchups · rank 1 of 38**
>
> Best `feraligatr_munkidori_damage_transfer` 97% · worst `team_rockets_persian_ex_attack_theft` 50%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box predates the ex audit and is not comparable**: that audit corrected typed-Energy scalers that counted the wrong Energy, discard-cost attacks that were never charged, and attack gates that were never enforced.
<!-- field-results -->






One of five decks built around the same-turn Special Condition stacking research in this repo
(see `combo_patterns.md` Pattern 5 and its "persistent vs. action-denial" refinement). This is
the most direct execution of that pattern: a Basic Pokémon line that guarantees a
**Paralyzed + Poisoned** stack on a single attack, no coin flip, paired with a scaler that
reads directly off however many Special Conditions are on the opponent's Active.

## Centerpieces

1. **Arbok** (Temporal Forces) — its attack inflicts Poisoned and Paralyzed on the opponent's
   Active unconditionally. Paralysis is the action-denial half (blocks the opponent's very next
   attack *and* retreat on its own, clears automatically after their turn); Poison is the
   persistent half that keeps ticking after Paralysis clears.

2. **Team Rocket's Muk** (Destined Rivals) — `Hazardous Venom` does 100 damage for each Special
   Condition currently affecting the opponent's Active. It doesn't need to reapply anything —
   it just cashes in whatever Arbok already guaranteed. `Gooped Up` is the backup Ability lock
   if Muk itself ends up Active.

3. **Roxie's Performance** (Supporter) — its real text is "During your opponent's next turn,
   their Poisoned Pokémon can't retreat" (an earlier draft of this writeup mis-described it as
   an applicator that inflicts Poisoned+Confused — corrected after re-checking the card's own
   rules text). It doesn't apply any condition itself; it extends the retreat-lock once
   Paralysis clears, so the opponent's Poisoned Active still can't just walk Hazardous Venom's
   target off the field.

## Design notes

- Team Rocket's Grimer/Muk is included as the evolution bridge and a second, slower way to
  reach the same Ability/attack combo if Muk alone doesn't draw first.
- Crushing Hammer disrupts the opponent's own Energy base while they're locked down and can't
  retreat away from the pressure.
- Hero's Cape (1x) is insurance against a snipe on a low-HP Muk before it fires Hazardous Venom.
- Verified with `check_energy_support.py`: mono-Darkness supply (14 Darkness Energy) covers
  every attack cost in the deck with no shortfalls; no attack-gating Ability text found.

## Pokémon TCG Live Import

```
Pokémon: 12
4 Ekans TEF 100
3 Arbok TEF 101
2 Team Rocket's Grimer DRI 123
3 Team Rocket's Muk DRI 124

Trainer: 34
4 Lillie's Determination MEG 119
4 Ultra Ball MEG 131
4 Buddy-Buddy Poffin MEG 167
3 Poké Pad ASC 198
3 Boss's Orders MEG 114
3 Roxie's Performance CRI 112
2 Night Stretcher MEG 173
2 Switch MEG 130
2 Air Balloon MEG 166
4 Crushing Hammer POR 71
2 Special Red Card CRI 113
1 Hero's Cape TEF 152

Energy: 14
14 Basic Darkness Energy

Total Cards: 60
```
