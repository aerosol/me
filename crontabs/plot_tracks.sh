#!/bin/bash
set -x
echo "START: $0"
cd /app/_dashboard && ./plot_tracks.sh && ./stats.py > index.html
cp -R dist $STATS_DEST_DIR
cp index.tml $STATS_DEST_INDEX
echo "END: $0"
