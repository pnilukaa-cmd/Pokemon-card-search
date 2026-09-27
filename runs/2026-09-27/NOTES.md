## What changed since the 2026-09-23 table

**The field.** 55 decks: the 54 of the previous run plus the user's
`ditto_tyranitar_gengar_hydreigon`. Same per-pair seeds (`rr1`), so a deck
in both runs faces the same dice against the same opponent.

**The engine** (commit in `ENGINE_COMMIT`). Every number in the previous
table predates all of these, so no deck's old figure is comparable:

- **Rules now enforced:** no Supporter on the first turn going first;
  no evolving on either player's first turn; no Stadium over one of the
  same name; mulligan extra draws.
- **Card conservation:** Knock Outs discard Energy, Tools and the
  Evolution stack; Stadium replacement; attack Bench searches;
  Run Away Draw no longer duplicates Dudunsparce (this inflated the
  Dudunsparce wall).
- **Deck orientation:** Seek Inspiration and the self-mill scalers read
  the top of the deck, not the bottom.
- **No peeking:** choosing an attack no longer reads hidden cards.
- **Every card effect modelled** (`audit_unmodeled.py`: 0): on-play and
  when-damaged Abilities, Prize modifiers, 66 attack texts, situational
  Trainers, Ability locks, 19 Tools, Special Energy and Stadium gaps.
- **Pilot (default greedy):** Basics and Items that reach the hand after
  the Supporter are played that turn; Rare Candy before Stage 1s.
