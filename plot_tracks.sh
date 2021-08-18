#!/bin/env sh
mkdir -p _activities-svg
for f in _activities/*.gpx
do
  echo "Processing $f"
  ./gpx2svg -i "$f" -o "$f.svg" -m 400
  echo "$(cat $f.svg)<hr/>" >> svgs.html
done

