#!/bin/env sh
mkdir -p _activities-svg
for f in _activities/*.gpx
do
  echo "Processing $f"
  ./gpx2svg -i "$f" -o _activities-svg/$(basename "$f.svg") -m 400
done

