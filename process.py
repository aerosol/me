#!/usr/bin/env python3

from pprint import pp
from collections import defaultdict
from pathlib import Path
import glob
import json
import os
import sys
import itertools
import time, datetime

def to_unix(s):
  return int(time.mktime(datetime.datetime.strptime(s,
      "%Y-%m-%dT%H:%M:%S.0").timetuple())) + 3600

def load_all(files):
    contents = []
    for f in files:
        with open(f) as json_file:
          contents.append(json.load(json_file))
    return contents

def flatten(stuff):
    return list(itertools.chain(*stuff))

def concat_objects(stuff):
    return list(itertools.chain(stuff))

def add_pk(obj, fn):
    obj['id'] = fn(obj)

datasets = defaultdict(list)

for filename in glob.iglob('2020-*/*.dat', recursive=True):
     kind = Path(filename).stem     
     datasets[kind].append(filename)

steps = flatten(load_all(datasets['steps']))
steps = list(
        map(
            lambda x: x.setdefault('id', to_unix(x['endGMT'])) and x, 
            steps))

sleep_data = load_all(datasets['sleep'])

sleep_activity_levels = flatten([s['sleepLevels'] for s in sleep_data])
sleep_activity_levels = [sal for sal in sleep_activity_levels if sal['activityLevel'] > 0.0]
sleep_activity_levels = list(
        map(
            lambda x: x.setdefault('id', to_unix(x['startGMT'])) and x, 
            sleep_activity_levels))


sleep_movements = flatten([s['sleepMovement'] for s in sleep_data])
sleep_movements = [sm for sm in sleep_movements if sm['activityLevel'] > 0.0]
sleep_movements = list(
        map(
            lambda x: x.setdefault('id', to_unix(x['startGMT'])) and x, 
            sleep_movements))


respirations = flatten([s.get('wellnessEpochRespirationDataDTOList') for s in
    sleep_data if s.get('wellnessEpochRespirationDataDTOList') is not None])
respirations = list(
        map(
            lambda x: x.setdefault('id', x['startTimeGMT']) and x, 
            respirations))

daily_sleep_data = concat_objects([s['dailySleepDTO'] for s in sleep_data])

heart = load_all(datasets['heart'])
heart_rates = flatten([s['heartRateValues'] for s in heart])
heart_rates = [
        {'timestamp': h[0] // 1000, 'rate': h[1], 'id': h[0] // 1000} 
        for h in heart_rates if h[1] is not None
        ]

with open('sqlite-input/steps.json', 'w') as outfile:
    json.dump(steps, outfile, sort_keys=True, indent=4)

with open('sqlite-input/sleep_activity_levels.json', 'w') as outfile:
    json.dump(sleep_activity_levels, outfile, sort_keys=True, indent=4)

with open('sqlite-input/sleep_movements.json', 'w') as outfile:
    json.dump(sleep_movements, outfile, sort_keys=True, indent=4)

with open('sqlite-input/respirations.json', 'w') as outfile:
    json.dump(respirations, outfile, sort_keys=True, indent=4)

with open('sqlite-input/daily_sleep_data.json', 'w') as outfile:
    json.dump(daily_sleep_data, outfile, sort_keys=True, indent=4)

with open('sqlite-input/heart_rates.json', 'w') as outfile:
    json.dump(heart_rates, outfile, sort_keys=True, indent=4)
