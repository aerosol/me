set -x
echo "START: $0"
cd /app && ./total_running_badge.sh $BADGE_PATH
curl -X PURGE $BADGE_CACHE_URL
echo "END: $0"
