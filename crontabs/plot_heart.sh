#!/bin/bash
set -x
echo "START: $0"
cd /app/scripts && ./run.sh && cp ./heart.png $HR_DEST_DIR
curl -X PURGE $HR_CACHE_URL
echo "END: $0"
