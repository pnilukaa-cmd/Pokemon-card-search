#!/bin/bash
# wait_fr.sh SUMMARY N: exit once SUMMARY has N result lines, or after 9 minutes.
f=$1; n=$2; end=$(( $(date +%s) + 540 ))
until [ "$(grep -c " over " $f 2>/dev/null || true)" -ge "$n" ] 2>/dev/null || [ $(date +%s) -ge $end ]; do sleep 5; done
grep ' over ' $f | tail -n +$3
