#!/bin/bash
# Copy the live checkpoints into checkpoint/ and push them.
cd "$(dirname "$0")/../.."
cp runs/2026-10-08/rr_*.json.partial runs/2026-10-08/checkpoint/ 2>/dev/null
n=$(python3 -c 'import json; print(len(json.load(open("runs/2026-10-08/checkpoint/rr_0.json.partial"))["results"]))')
git add runs/2026-10-08/checkpoint && git commit -qm "Field rerun 2026-10-08: checkpoint, $n of ~732 pairings per shard

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Js4QknU7MxkkatMjsa29yV" || exit 0
for i in 1 2 3 4; do git push -u origin claude/code-restructuring-yo2673 >/dev/null 2>&1 && break; sleep $((2**i)); done
