#!/bin/bash
# Checkpoint every 30 minutes until all four shards have written rr_N.json.
cd "$(dirname "$0")/../.."
while [ "$(ls runs/2026-10-25/rr_[0-3].json 2>/dev/null | wc -l)" -lt 4 ]; do
  sleep 1800
  bash runs/2026-10-25/checkpoint.sh
done
