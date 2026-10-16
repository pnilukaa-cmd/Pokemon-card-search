#!/bin/bash
# round.sh BASE PREFIX -- write the round's variants of BASE as PREFIX_<name>.txt
S=/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad/gg
B=$1; P=$2; cd $S
v() { n=$1; shift; python3 variant.py $B ${P}_$n.txt "$@" && echo ${P}_$n.txt; }
E="Basic Darkness Energy"
v tox0   "Toxel PFL 67:-2" "Toxtricity PFL 68:-2" "$E:+4"
v munk0  "Munkidori ASC 99:-2" "$E:+2"
v pech1  "Pecharunt ex SFA 39:-1" "$E:+1"
v pad2   "Poké Pad POR 81:-2" "$E:+2"
v cape   "Unfair Stamp TWM 165:-1" "Hero's Cape TEF 152:+1"
v janine "Drayton SSP 174:-2" "Janine's Secret Art SFA 59:+2"
v tef3   "Gengar ex 30C 90:-3" "Gengar ex TEF 104:+3"
v tef1   "Gengar ex 30C 90:-1" "Gengar ex TEF 104:+1"
v haunt  "Haunter ASC 124:-4" "Haunter POR 49:+4"
v ruins  "Poké Pad POR 81:-2" "Risky Ruins MEG 127:+2"
v helmet "Poké Pad POR 81:-1" "Punk Helmet PFL 121:+1"
v shadow "$E:-2" "Shadowy Darkness Energy PBL 83:+2"
v candy4 "Rare Candy MEG 125:+2" "Poké Pad POR 81:-2"
v e2     "$E:+2" "Drayton SSP 174:-2"
v legacy "Unfair Stamp TWM 165:-1" "Legacy Energy TWM 167:+1"
v gen4   "Gengar ex 30C 90:+1" "$E:-1"
v mega3  "Mega Gengar ex ASC 125:+1" "$E:-1"
