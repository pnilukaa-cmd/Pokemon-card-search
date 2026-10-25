#!/bin/bash
# Copy the live checkpoints into checkpoint/ and push them.
cd "$(dirname "$0")/../.."
cp runs/2026-10-25/rr_*.json.partial runs/2026-10-25/checkpoint/ 2>/dev/null
n=$(python3 -c 'import json,glob; print(sum(len(json.load(open(f))["results"]) for f in glob.glob("runs/2026-10-25/checkpoint/rr_*.json.partial")))')
git add runs/2026-10-25/checkpoint && git commit -qm "Field rerun 2026-10-25: checkpoint, $n of 4656 pairings

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01Js4QknU7MxkkatMjsa29yV" || exit 0
for i in 1 2 3 4; do git push -u origin claude/code-restructuring-yo2673 >/dev/null 2>&1 && break; sleep $((2**i)); done
