#!/usr/bin/env python3

from garminconnect import (
    Garmin,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
    GarminConnectAuthenticationError,
)

from datetime import date

import json
import logging
import os
import sys

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) == 1:
    isodate = date.today().isoformat()
elif len(sys.argv) == 2:
    isodate = sys.argv[1]

os.makedirs(isodate, exist_ok=True)

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

activities = client.get_activities(0,10) 
for activity in activities:
        activity_id = activity["activityId"]
        csv_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.CSV)
        output_file = f"%s/activity_{str(activity_id)}.csv" % isodate
        with open(output_file, "wb") as fb:
          fb.write(csv_data)

sleep = client.get_sleep_data(isodate)
with open('%s/sleep.dat' % isodate, 'w') as outfile:
    json.dump(sleep, outfile, sort_keys=True, indent=4)
