# Mega Dragonite ex / Kangaskhan ex / Salazzle ex screens, 2026-10-23

A submitted list (`user_raw.txt` as pasted; `lists/D_user.txt` with the
pool's printings: Pokégear 3.0 BLK 84 and Rare Candy MEG 125 for the SVI
printings, "6 Basic {R} Energy MEE 10" as Basic Fire Energy). The question
was what the strategy is.

All runs are against the 94-deck field, paired on the same seeds within a
tag. Screens are 200 games per opponent; the confirmation is 1000.

**Tags.**
- `dn0`: engine 044bae0 (heals fixed). The submitted list measured 20.68%,
  then 44.05% with the Sky Transport fix (6a923e9); the field has no Sky
  Transport, so the pair is on one tag. These two result files were lost
  in a container restart; the numbers are in commit 6a923e9.
- `dn1`: engine 6a923e9. Round 1 (`d1_`, from `D_user`) and round 2
  (`d2_`, from `d1_e6`), plus the heal_cost_aware probe (`K_*_heal`) and
  its field check (`hc/`).
- `dn2`: + heal_cost_aware on. Rounds 3-5 (`d2_` singles re-run, `d3_`,
  `d4_`, `d5_`), the typed_attach probe (`ta/` lists, `K_*` with
  `PROBE_KNOBS=typed_attach=1`), and the 1000-game confirmation (`D_user`,
  `d3_gemfanwal`, `d5_boss0`).
- `dn3`: engine e8b2d1a (typed_attach on, Curly Wall / Lively Stadium /
  Tool fixes). The final and submitted lists re-confirmed at 1000, the
  Ryuno Glide variant and the Gengar list's Powerglass re-screened, and the
  submitted Snorlax list's first run (`X_user`).

**Rounds** (each paired against the best list of the round before):
- `d1_` from `D_user`: Energy for everything. Best `d1_e6` (12 Energy).
- `d2_` from `d1_e6`. `d3_` combinations from `d1_e6`; best `d3_gemfanwal`.
- `d4_` from `d3_gemfanwal`; best `d4_boss1`. `d5_` from `d4_boss1`; best
  `d5_boss0`, the final list.

**Scripts:** `variant.py BASE OUT 'Card SET NUM:+n' ...` (keeps 60, reads
sections from the card file) and `boardgame.py LIST OPP SEED` (one verbose
game with your board printed each turn; it found the Sky Transport
ping-pong and the Energy starvation).

Write-up: `decks/mega_dragonite_kangaskhan_salazzle_wall.md`.
