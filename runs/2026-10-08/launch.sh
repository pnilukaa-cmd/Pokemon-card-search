#!/bin/bash
# Start (or resume) the 2026-10-08 field run: 4 shards, 1000 games, tag rr1.
cd "$(dirname "$0")/../.."
for i in 0 1 2 3; do
  setsid nohup python3 roundrobin.py decks/field runs/2026-10-08/rr_$i.json $i 4 1000 rr1 \
      >> runs/2026-10-08/log_$i.txt 2>&1 < /dev/null &
done
