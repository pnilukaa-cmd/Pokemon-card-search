#!/bin/bash
# usage: run_list_wt.sh <tree> <suffix> <tag> <games> <summary> deck.txt...
# Same as run_list.sh, run from <tree>, with the caller's PILOT/PROBE_KNOBS
# environment; outputs are named <deck>_<suffix>_<tag>_<games>.
SP=/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad/tr
cd $1; suf=$2; tag=$3; games=$4; summ=$5; shift 5
for f in "$@"; do
  b=$(basename $f .txt)_$suf
  s=$(date +%s)
  JOBS=4 python3 vs_field.py $f /home/user/Pokemon-card-search/decks/field $games $tag $SP/out/${b}_${tag}_${games}.json > $SP/out/${b}_${tag}_${games}.log 2>&1
  echo "$b $(( $(date +%s)-s ))s $(grep -E '^[^ ]+: [0-9.]+%' $SP/out/${b}_${tag}_${games}.log | head -1)" >> $SP/$summ
done
echo DONE >> $SP/$summ
