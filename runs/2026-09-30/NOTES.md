## What changed since the 2026-09-29 table

**The field.** The same 57 decks and per-pair seeds (`rr1`). One list
changed: `ditto_transform_hydreigon` plays Hero's Cape instead of Secret
Box (+2.75 +/- 0.36 paired against the field before this run).

**The engine** (commit in `ENGINE_COMMIT`): the Ability-lock cache no
longer hands a reused dict address another deck's "no locks" (Flutter
Mane, Iron Thorns ex, Watchtower, Gastrodon could lose their locks
between pairings). Only decks with an Ability lock, and their opponents,
can move for that reason.
