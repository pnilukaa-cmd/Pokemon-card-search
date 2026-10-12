# Cinderace shell on every Energy type, 2026-10-12 (in progress)

The question: does the Cinderace / two-big-Basics build work better on an
Energy type other than Fighting?

`lists/gen.py` writes one list per type with the same frame as the
Fighting list:
- 4 Cinderace, 2 main hitters, 1 second hitter, 1 Mega Audino ex.
- The same generic Trainers.
- 21-23 Basic Energy plus the type's Special Energy.

Fighting Gong, Premium Power Pro and Core Memory have no counterpart on
other types, so the type lists use 4 Ultra Ball and the type's own
support. `F_ctl_ub` is the Fighting list built the same way, for an
apples-to-apples comparison.

200 games against each of the 86 field decks (tag et1), paired on the
same seeds. Results in `summary.txt` and `results/`.
