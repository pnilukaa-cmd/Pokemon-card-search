# festival_lead — TCGplayer, September 2026

<!-- field-results -->
> ### Field results — 2026-09-13
> **36.4% mean · 35.5% median · 6 of 43 winning matchups · rank 39 of 44**
>
> Best `meta_ns_zoroark` 80% · worst `orthworm_ex_metal_retaliation` 10%.
>
> Full round robin, 200 games per pairing, every deck against every other — see [FIELD_RESULTS.md](FIELD_RESULTS.md). **Any win rate written in the body below this box was measured on an older engine and is not comparable** — not with this number and not with each other.
<!-- field-results -->






**Not my list.** From Natalie Millar's *The Best Pokémon TCG Decks Right
Now (September 2026)* on TCGplayer (2026-08-25), reproduced card-for-card.

The published lists give collector numbers without set codes, so every
line was resolved by number against this repo's pool. Basic Energy is
written without a set code, as everywhere else here.

`Thwackey`'s `Boom Boom Groove` feeding the Festival Lead Abilities on
`Dipplin` and `Seaking`. The engine of the deck is `Festival Lead` itself:
*"if Festival Grounds is in play, this Pokémon may use an attack it has
twice."* That is two `Do the Wave`s a turn off one Grass Energy.

**Rank 39 of 44 at 36.0%, and that is after the fix that made the deck
work at all.** `Festival Grounds` was never being played, because the
engine only put a Stadium down if the Stadium's OWN text did something it
modelled — and Festival Grounds' printed effect is Special Condition
immunity, which compiled to nothing. So the gate was never open, the
double attack never fired, and this deck dealt exactly half its damage in
every game it ever played here. Against `meta_dragapult_pure` over 400
games it went from **5.0% to 32.5%** once the Stadium reached the table:
556 grants, 1075 second swings that land. The archetype is real; 36th
percentile is what a two-swing 130 looks like against a field of
one-swing 250s when nobody is sequencing.

**One claim from the article does not survive the arithmetic.** It rates
the Prize trade as the format's most efficient on the strength of
`Dipplin` one-shotting an unmodified `Mega Excadrill ex` through its
Grass Resistance. `Mega Excadrill ex` is 340 HP with `-30` Grass
Resistance, and `Do the Wave` on a full Bench is 100, +30 from
`Brave Bangle` (the attacker has no Rule Box and the target is an ex),
+30 from `Kieran`'s damage mode, −30 Resistance = **130 a swing, 260 for
both swings**. It is a clean two-turn Knock Out, not a one-shot.

## Decklist

```
Pokémon: 22
4 Grookey TWM 14
4 Thwackey TWM 15
4 Dipplin TWM 18
2 Applin TWM 17
2 Applin TWM 126
2 Goldeen TWM 44
1 Seaking PRE 21
1 Shaymin DRI 10
1 Rellor TEF 23
1 Rabsca TEF 24

Trainer: 32
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad ASC 198
4 Lillie's Determination ASC 192
4 Festival Grounds TWM 149
3 Ultra Ball MEG 131
2 Night Stretcher ASC 196
2 Gladion's Final Battle PBL 77
2 Boss's Orders MEG 114
2 Brave Bangle WHT 80
2 Air Balloon BLK 79
1 Kieran TWM 154
1 Switch MEG 130
1 Secret Box TWM 163

Energy: 6
4 Growing Grass Energy POR 86
2 Basic Grass Energy

Total Cards: 60
```
