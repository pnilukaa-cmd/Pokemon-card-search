# Pending — nine lists awaiting the 30th Celebration data

**Not my lists.** Supplied by the user from a pastebin dated 2026-09-14,
held here until the card data exists. No fenced decklist per deck on
purpose: several do not resolve, and `check_decks.py` would be right to
reject them.

## Status, checked 2026-09-16 (30th Celebration's release day)

The set is live in the Pokemon TCG app. It is **not** in this pool, and
today's authoritative `fetch_pokemon_cards.py --check` says why:

```
regulationMark:K: 0 cards, nothing to add
regulationMark:L: 0 cards, nothing to add
--check: 1964 records fetched (1389 distinct names) vs 1964 on disk
  new names: 0
  names on disk but not fetched: 0
```

`api.pokemontcg.io`, the source this pool is built from, has not indexed
it — its newest set is still `PBL` (2026-07-17) and a
`set.name:"30th Celebration"` query returns 0. That lag between the game
client and the community API is normal. Every other card source is refused
by the network egress proxy at CONNECT.

## What actually blocks each list

Only **six cards** block anything, all Pokemon from sets not yet in the
pool. Nearly all the apparent breakage was Basic Energy written with the
`MEE` set code — that is the 30th Celebration foil Basic Energy subset,
and Basic Energy carries **no set code** in this repo. Rewrite
`4 Psychic Energy MEE 5` as `4 Basic Psychic Energy` and it resolves.

| deck | resolves | blocked by |
|---|---|---|
| `mew_bunny` | 58/60 | `Mew ex` **M6a 57** |
| `umbreon` | 60/60 | — none |
| `unown` | 59/60 | `Unown` **M6a 60** |
| `greninja` | 59/60 | `Greninja ex` **M6a 15** |
| `mew_mega` | 58/60 | `Mew ex` **M6a 57** |
| `exeggutor` | 57/60 | `Alolan Exeggutor` **MP 148** |
| `sylveon` | 60/60 | — none |
| `gengar` | 57/60 | `Gengar ex` **M6a 76** |
| `salamence` | 58/60 | `Salamence ex` **M6a 88** |

`umbreon` and `sylveon` reach a full 60 — but see the warning below before
treating that as ready.

## Two silent mis-resolutions, which matter more than the blockers

`MP` and `MF` are not Standard set codes, and the resolver falls back to
matching on NAME alone. That does not fail loudly; it returns a different
card:

| written | silently resolved to |
|---|---|
| `3 Sylveon ex MP 153` | **Sylveon ex SSP 86** |
| `3 Umbreon ex MF 17` | **Umbreon ex PRE 161** |

Those may or may not be the intended cards. `sylveon` and `umbreon`
"fully resolving" is therefore not evidence they are correct — it is the
fallback hiding two unknown set codes. Both need checking against the
physical cards before either list is measured.

`1 Lillie's Clefairy ex JTG 56` also resolves to **ASC 280**, but that one
is a genuine listed reprint of the same card rather than a fallback.

## When the data lands

1. `python3 fetch_pokemon_cards.py --check` — reports what would change,
   writes nothing, and warns if 30C shipped under a regulation mark
   outside `ACTIVE_REGULATION_MARKS`.
2. Add the set, then resolve `M6a` and `MP` against real printings.
3. `Mew ex`'s **Memory Helix** ("use the attacks of any of your Benched
   Pokemon") is the same shape as `N's Zoroark ex`'s Night Joker. The
   copy-attack machinery is built and exercised; only the rule that
   recognises the text is missing.
4. 30C is tournament legal from **2026-09-25**.

## The lists as supplied

### mew_bunny

```text
Pokémon: 19
4 Dunsparce JTG 120
3 Dudunsparce TEF 129
1 Dudunsparce ex JTG 121
3 Buneary PFL 83
3 Mega Lopunny ex PFL 84
2 Mew ex M6a 57
1 Fan Rotom ASC 171
1 Lillie's Clefairy ex ASC 76
1 Chien-Pao SSP 56
Trainer: 32
4 Lillie's Determination ASC 192
3 Hilda WHT 84
3 Wally's Compassion MEG 132
3 Boss's Orders ASC 183
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
3 Ultra Ball ASC 213
2 Wondrous Patch PFL 94
1 Pokégear 3.0 BLK 84
2 Air Balloon BLK 79
3 Battle Cage PFL 85
Energy: 9
4 Psychic Energy MEE 5
4 Mist Energy TEF 161
1 Enriching Energy SSP 191
```

### umbreon

```text
Pokémon: 17
3 Eevee SFA 50
3 Umbreon ex MF 17
2 Toxel PFL 67
2 Toxtricity PFL 68
2 Munkidori ASC 99
2 Pecharunt ex SFA 39
1 Chi-Yu PBL 59
1 Fezandipiti ex ASC 142
1 Pecharunt PR-SV 149
Trainer: 33
4 Lillie's Determination ASC 192
3 Boss's Orders MEG 114
2 Judge POR 76
2 Team Rocket's Petrel ASC 207
4 Ultra Ball ASC 213
4 Buddy-Buddy Poffin ASC 184
4 Pokégear 3.0 BLK 84
2 Poké Pad POR 81
1 Unfair Stamp TWM 165
1 Energy Recycler DRI 164
1 Night Stretcher ASC 196
2 Binding Mochi PRE 95
1 Air Balloon ASC 181
2 Team Rocket's Watchtower ASC 210
Energy: 10
10 Darkness Energy MEE 7
```

### unown

```text
Pokémon: 22
4 Slowpoke SCR 57
3 Slowking SCR 58
3 Mega Kangaskhan ex MEG 104
2 Latias ex SSP 76
2 Metagross CRI 61
2 Kyurem SFA 47
1 Annihilape SSP 100
1 Annihilape PBL 41
1 Unown M6a 60
1 Fezandipiti ex ASC 142
1 Lillie's Clefairy ex ASC 76
1 Meowth ex POR 62
Trainer: 28
4 Lillie's Determination ASC 192
4 Ciphermaniac's Codebreaking PRE 104
4 Ultra Ball ASC 213
4 Poké Pad POR 81
3 Wondrous Patch PFL 94
3 Night Stretcher SFA 61
1 Switch MEG 130
1 Prime Catcher PRE 119
4 Academy at Night SFA 54
Energy: 10
4 Telepathic Psychic Energy POR 88
4 Psychic Energy MEE 5
2 Boomerang Energy TWM 166
```

### greninja

```text
Pokémon: 19
4 Froakie CRI 20
2 Frogadier CRI 21
2 Mega Greninja ex CRI 22
1 Greninja ex M6a 15
1 Greninja ex TWM 106
2 Dunsparce JTG 120
1 Dunsparce PRE 79
3 Dudunsparce PRE 80
1 Dudunsparce ex JTG 121
1 Budew ASC 16
1 Fezandipiti ex ASC 142
Trainer: 32
4 Lillie's Determination ASC 192
3 Hilda WHT 84
2 Boss's Orders ASC 183
1 Judge POR 76
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
2 Ultra Ball ASC 213
1 Special Red Card CRI 82
1 Night Stretcher ASC 196
1 Energy Retrieval WHT 82
2 Air Balloon BLK 79
3 Surfing Beach MEG 129
Energy: 9
7 Water Energy MEE 3
1 Neo Upper Energy TEF 162
1 Ignition Energy WHT 86
```

### mew_mega

```text
Pokémon: 18
2 Mew ex M6a 57
2 Mega Audino ex ASC 172
2 Mega Kangaskhan ex MEG 104
2 Mega Absol ex MEG 86
2 Munkidori ASC 99
1 Yveltal MEG 88
2 Pecharunt ex SFA 39
1 Fezandipiti ex ASC 142
1 Moltres PFL 14
1 Lillie's Clefairy ex ASC 76
1 Meowth ex POR 62
1 Latias ex SSP 76
Trainer: 29
4 Lillie's Determination ASC 192
3 Boss's Orders ASC 183
2 Brock's Scouting JTG 146
2 Crispin PRE 105
4 Mega Signal MEG 121
4 Ultra Ball ASC 213
2 Night Stretcher ASC 196
2 Energy Switch MEG 115
1 Special Red Card CRI 82
2 Pokégear 3.0 BLK 84
1 Hero's Cape TEF 152
1 Team Rocket's Watchtower ASC 210
1 Lively Stadium SSP 180
Energy: 13
7 Darkness Energy MEE 7
3 Mist Energy TEF 161
2 Psychic Energy MEE 5
1 Fire Energy MEE 2
```

### exeggutor

```text
Pokémon: 19
2 Exeggcute SSP 1
2 Exeggcute MEG 4
3 Alolan Exeggutor MP 148
4 Teal Mask Ogerpon ex TWM 25
3 Chikorita MEG 8
2 Bayleef MEG 9
2 Meganium MEG 10
1 Fezandipiti ex ASC 142
Trainer: 30
4 Lillie's Determination ASC 192
2 Gwynn PBL 78
2 Boss's Orders ASC 183
1 Lana's Aid TWM 155
4 Energy Switch MEG 115
4 Bug Catching Set PRE 102
4 Poké Pad POR 81
2 Ultra Ball ASC 213
2 Jumbo Ice Cream PFL 91
1 Night Stretcher ASC 196
1 Hero's Cape TEF 152
3 Forest of Vitality ASC 188
Energy: 11
11 Grass Energy MEE 1
```

### sylveon

```text
Pokémon: 18
4 Eevee SFA 50
3 Sylveon ex MP 153
4 Team Rocket's Tarountula ASC 18
4 Team Rocket's Spidops ASC 19
1 Lillie's Clefairy ex JTG 56
1 Fezandipiti ex ASC 142
1 Meowth ex POR 62
Trainer: 31
4 Lillie's Determination ASC 192
2 Crispin PRE 105
2 Boss's Orders MEG 114
2 Team Rocket's Petrel ASC 207
4 Energy Switch MEG 115
4 Buddy-Buddy Poffin ASC 184
4 Ultra Ball ASC 213
3 Poké Pad POR 81
2 Wondrous Patch PFL 94
1 Night Stretcher ASC 196
1 Energy Search Pro SSP 176
1 Air Balloon ASC 181
1 Prism Tower CRI 80
Energy: 11
4 Psychic Energy MEE 5
1 Grass Energy MEE 1
1 Fire Energy MEE 2
1 Water Energy MEE 3
1 Lightning Energy MEE 4
1 Fighting Energy MEE 6
1 Darkness Energy MEE 7
1 Metal Energy MEE 8
```

### gengar

```text
Pokémon: 20
4 Gastly POR 48
2 Haunter ASC 124
3 Gengar ex M6a 76
1 Mega Gengar ex ASC 125
2 Toxel PFL 67
2 Toxtricity PFL 68
2 Munkidori ASC 99
1 Tatsugiri TWM 131
1 Shaymin DRI 10
1 Chi-Yu PBL 59
1 Pecharunt ex SFA 39
Trainer: 31
4 Lillie's Determination ASC 192
2 Boss's Orders MEG 114
2 Team Rocket's Petrel DRI 176
4 Rare Candy MEG 125
4 Buddy-Buddy Poffin ASC 184
4 Ultra Ball ASC 213
3 Poké Pad POR 81
1 Night Stretcher ASC 196
1 Unfair Stamp TWM 165
1 Special Red Card CRI 82
1 Energy Recycler DRI 164
2 Air Balloon ASC 181
2 Team Rocket's Watchtower ASC 210
Energy: 9
9 Darkness Energy MEE 7
```

### salamence

```text
Pokémon: 20
4 Dreepy ASC 158
4 Drakloak ASC 159
2 Dragapult ex ASC 160
2 Bagon JTG 112
1 Shelgon JTG 113
2 Salamence ex M6a 88
1 Fezandipiti ex ASC 142
1 Meowth ex POR 62
1 Budew ASC 16
1 Patrat CRI 70
1 Moltres PFL 14
Trainer: 31
4 Lillie's Determination ASC 192
3 Crispin PRE 105
2 Boss's Orders MEG 114
1 Rosa's Encouragement POR 84
1 Judge POR 76
4 Buddy-Buddy Poffin ASC 184
4 Poké Pad POR 81
3 Rare Candy MEG 125
3 Ultra Ball ASC 213
1 Unfair Stamp TWM 165
2 Night Stretcher ASC 196
1 Special Red Card CRI 82
1 Air Balloon ASC 181
1 Team Rocket's Watchtower ASC 210
Energy: 9
4 Fire Energy MEE 2
3 Water Energy MEE 3
2 Psychic Energy MEE 5
```
