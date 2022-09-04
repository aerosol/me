#!/bin/sh
echo "Writing env"
printenv
printenv > /etc/environment
echo "Done. Running scripts."
/app/crontabs/run_daily_dump.sh
/app/crontabs/backfill_yesterday.sh
/app/crontabs/plot_tracks.sh
/app/crontabs/plot_heart.sh
/app/crontabs/generate_badge.sh
echo "Running crond."
/usr/sbin/crond -f -l 8
