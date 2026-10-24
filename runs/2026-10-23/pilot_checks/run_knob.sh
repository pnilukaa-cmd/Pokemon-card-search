#!/bin/bash
# usage: run_knob.sh <tag> <games> <summary> <probe knobs> deck.txt...
# Runs each deck under PILOT=probe with PROBE_KNOBS; output named <deck>__<knobs>.
cd /home/user/Pokemon-card-search
SP=/tmp/claude-0/-home-user-Pokemon-card-search/32313191-2e9b-5f12-921b-86b3863481b6/scratchpad/tr
tag=$1; games=$2; summ=$3; knobs=$4; shift 4
k=$(echo "$knobs" | tr '=,' '_-')
for f in "$@"; do
  b=$(basename $f .txt)__$k
  s=$(date +%s)
  PILOT=probe PROBE_KNOBS="$knobs" JOBS=4 python3 vs_field.py $f decks/field $games $tag $SP/out/${b}_${tag}_${games}.json > $SP/out/${b}_${tag}_${games}.log 2>&1
  echo "$b $(( $(date +%s)-s ))s $(grep -E '^[^ ]+: [0-9.]+%' $SP/out/${b}_${tag}_${games}.log | head -1)" >> $SP/$summ
done
echo DONE >> $SP/$summ
