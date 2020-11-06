#!/usr/bin/env python3

import sys
import json
import csv

from datetime import date, timedelta

yesterday = (date.today() - timedelta(1)).isoformat()
today = date.today().isoformat()

spamwriter = csv.writer(sys.stdout)

def dump(ts):
    with open("../%s/heart.dat" % ts) as json_file:
        data = json.load(json_file)
        for row in data['heartRateValues']:
            ts = row[0] // 1000
            bpm = row[1]
            spamwriter.writerow([ts, bpm])

dump(yesterday)
dump(today)
