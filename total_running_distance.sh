#!/bin/env sh
cat _activities/*.json | jq -c '. | select(.activityType.typeKey ==
"running")' | jq -n '[inputs | .distance] | add'
