# smart_search, 2026-10-11

200 games x 83 opponents, tag ss1, paired on the same seeds.

- `__s0`: knob off for everyone (baseline).
- `__s1` / `__s2`: knob on for EVERY player (env SMART_SEARCH=1 / 2). The
  field improves too, so these sum to about zero across a whole field and
  only re-rank decks: +0.51 / +0.45 on average over these ten.
- `__p1` / `__p2`: knob on for the measured deck only (PILOT=probe,
  PROBE_KNOBS=smart_search=1 / 2). This is the measurement that decides:
  setting 1 better on all 10 decks, +2.62 on average; setting 2 no better.

Setting 1 is now the default.
