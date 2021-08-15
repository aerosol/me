#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date, timedelta

import json
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) == 1:
    isodate = date.today().isoformat()
elif len(sys.argv) == 2:
    if sys.argv[1] == 'yesterday':
        isodate = (date.today() - timedelta(1)).isoformat()
    else:
        isodate = sys.argv[1]

os.makedirs(isodate, exist_ok=True)
os.makedirs('_activities', exist_ok=True)

email = os.environ['GARMIN_EMAIL']
password = os.environ['GARMIN_PASS']

client = Garmin(email, password)
client.login()

stats = client.get_stats(isodate)
with open('%s/stats.dat' % isodate, 'w') as outfile:
    json.dump(stats, outfile, sort_keys=True, indent=4)

steps = client.get_steps_data(isodate)
with open('%s/steps.dat' % isodate, 'w') as outfile:
    json.dump(steps, outfile, sort_keys=True, indent=4)

heart = client.get_heart_rates(isodate)
with open('%s/heart.dat' % isodate, 'w') as outfile:
    json.dump(heart, outfile, sort_keys=True, indent=4)

def dump_activities():
    with open('last_activity_seq.txt', 'r+') as lasf:
        las = int(lasf.read().strip())
        last_activity_seq = las

        activities = client.get_activities(last_activity_seq, last_activity_seq + 10) 
        if activities:
            for activity in activities:
                    las+=1
                    activity_id = activity["activityId"]
                    csv_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.CSV)
                    output_file = f"_activities/activity_{str(activity_id)}.csv"
                    with open(output_file, "wb") as fb:
                      fb.write(csv_data)

            lasf.seek(0)
            lasf.write(str(las))
            lasf.truncate()
            dump_activities()

dump_activities()

sleep = client.get_sleep_data(isodate)
with open('%s/sleep.dat' % isodate, 'w') as outfile:
    json.dump(sleep, outfile, sort_keys=True, indent=4)
