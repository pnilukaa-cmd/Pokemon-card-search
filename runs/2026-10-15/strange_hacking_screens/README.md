# Strange Hacking / six-Prize screens, 2026-10-15

A submitted list (`user_raw.txt` as pasted; `U_user` imported with
`import_decklist.py`) tagged "taking 6 Prizes in one turn". The questions:
how does that turn work, and what supports it?

All runs: tag sx0, against the 92-deck field, paired on the same seeds.
Screens are 200 games per opponent; the confirmation is 1000.

**Runs:**
- `U_user_head`: the submitted list on the engine before the Strange
  Hacking fix (worktree of HEAD), to measure the fix.
- `s1_`: support cards and Nighttime Mine, from `U_user`.
- `s2_` from `s1_mine0`, `s3_` from `s2_fros22`, `s4_` from `s3_fros0`,
  `s5_` from `s4_bh`. The final list is `s5_candy`.
- `F_pure`: a Froslass build with no Abilities of its own (TWM Kadabra and
  Alakazam only, 4-4 Froslass).
- **Confirmation:** 1000 games for `U_user`, `s3_bh` (the best that keeps
  Froslass) and `s5_candy`.

**Scripts:**
- `potential.py LIST N`: at each of the list's attacks, the counters on the
  opponent's board and the most Prizes one Strange Hacking could take with
  them. Results for each variant are in `potential/`.
- `bigturn.py LIST N`: the most Prizes the list actually took in one turn,
  and what each Strange Hacking took.

Write-up: `decks/alakazam_munkidori_strange_hacking.md`.
