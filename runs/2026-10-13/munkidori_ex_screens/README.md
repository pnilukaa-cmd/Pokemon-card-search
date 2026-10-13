# Munkidori ex screens, 2026-10-13

Brief: "a random ex Pokémon with an Ability; devise a strategy from it,
with supporting win conditions". Rolled among the 40 ex-with-Ability
Pokémon no field deck played: Munkidori ex SFA 37.

All runs: tag mk0, against the 91-deck field, paired on the same seeds.
Screens are 200 games per opponent; the confirmation is 1000.

**Start lists:**
- `A_loyal`: 4 Munkidori ex, 2 Pecharunt ex, 2 Okidogi ex, 1 Fezandipiti
  ex, 2 Munkidori.
- `B_fez`: no Okidogi ex.
- `C_okidogi3`: 3 Okidogi ex, 2 Fezandipiti ex, no Munkidori.
- `D_legacy`: A with Legacy Energy.

**Tuning:** rounds `m1_` from C, `m2_` from `m1_oki4`, `m3_` from
`m2_combo`. The final list is `m3_fez0`.

**Controls:** `X_nomunk` (no Munkidori ex) and `X_munk2` (2 Munkidori ex).

**Confirmation:** 1000 games for `m3_fez0`, `A_loyal` and `X_nomunk`.

`kocount.py LIST N` counts the Prizes the opponent took for each Knock Out
of the deck's ex Pokémon (Munkidori ex's Prize cut).

Write-up: `decks/munkidori_ex_pecharunt_chains.md`.
