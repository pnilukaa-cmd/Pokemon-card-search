# Snorlax / Bouffalant screens, 2026-10-23

A submitted list (`user_raw.txt` as pasted; imported as `lists/X_user.txt`
with the pool's printings of the four rotated cards), reviewed as the
earlier submitted lists were: validate, check the engine, measure, tune,
confirm. Write-up: `decks/snorlax_bouffalant_kangaskhan_curly_wall.md`.

All against the 95-deck field, paired on the same seeds within a tag.
Screens are 200 games per opponent; the confirmation is 1000.

**Tags:**
- `sx1`: d6f6f1c.
- `hp1`: a569a0d. Switch waits for a better attacker, worth +12.39 on this
  list (`../pilot_checks`).
- `hp2`: f01e13e.

**Rounds** (each paired against the best list of the round before):
- `s1_` from `X_user` (sx1): every cut for a Psychic Energy.
- `s2_` from `X_user` (hp1): combinations. Some `s1_` lists re-run on hp1.
- `s3_` from `s3_base` (hp2).
- `s4_` from `s4_base` (hp2). Best: `s4_kang2`.
- `s5_` from `s4_kang2` = `s5_base` (hp2). Best: `s5_kang4`, the final list.
- `s6_` from `s5_kang4` (hp2). Nothing kept.
- **Confirmation:** 1000 games on hp2 for `X_user` and `s5_kang4`.

**Scripts:**
- `variant.py BASE OUT 'Card SET NUM:+n' ...` writes a variant that stays at 60.
- `boardgame.py LIST OPP SEED [knobs]` plays one verbose game and prints
  your board each turn.
