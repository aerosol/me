#!/bin/env sh
mkdir -p dist/_activities-svg
for f in ../_activities/*.gpx
do
  echo "Processing $f"
  ./gpx2svg -i "$f" -o dist/_activities-svg/$(basename "$f.svg") -m 400
done

