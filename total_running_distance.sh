#!/bin/env sh
echo "$(cat _activities/*.json | jq -c '. | select(.activityType.typeKey ==
"running")' | jq -n '[inputs | .distance] | add') / 1000" | bc
