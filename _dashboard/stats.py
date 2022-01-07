#!/usr/bin/env python3

from datetime import datetime
import dateutil.parser as dparser
from datetime import timedelta
import json
import os
import sys
import glob
import string
from datetime import date

CURRENT_YEAR = date.today().year

activities = []

for name in glob.glob('../_activities/*.json'):
    with open(name, 'r') as activity:
        obj = json.loads(activity.read())
        activities.append(obj)

def maximum(activities, activity_type, field):
    return max(a[field] for a in activities if a['activityType']['typeKey'] == activity_type and a[field] is not None)

def summary(activities, activity_type, field):
    return sum(a[field] for a in activities if a['activityType']['typeKey'] == activity_type)

def summary_this_year(activities, activity_type, field):
    this_year = [a for a in activities if a['startTimeGMT'].startswith('%d' %
        CURRENT_YEAR)]
    return summary(this_year, activity_type, field)

def distinct_active_days(activities):
    return len(set([a['startTimeGMT'][0:10] for a in activities if a['startTimeGMT'].startswith('%d' % CURRENT_YEAR)]))

def most_recent(activities, activity_type):
    return [a for a in sorted(activities, key=lambda x: x['activityId']) if a['activityType']['typeKey'] ==
            activity_type][-1]

def svg_gpx(activity):
    distance = activity['distance'] / 1000
    return """
    %.2f km<br/>
    <img class="w-3/4" src="dist/_activities-svg/activity_%s.gpx.svg"/>
    """ % (distance, activity['activityId'])

def vo2_max_widget(activities):
    max_vo2_max = str(maximum(activities, 'running', 'vO2MaxValue'))
    current = str(most_recent(activities, 'running')['vO2MaxValue'])
    svg = svg_vo2max(activities)
    html = """
    <span class="text-xs w-full">
    <span class="text-gray-500 font-normal mr-2">Peak:&nbsp;<span class="text-black font-bold">%s</span></span>
    <span class="text-gray-500 font-normal">Current:&nbsp;<span class="text-black font-bold">%s</span></span>
    </span>
    %s
    """ % (max_vo2_max, current, svg)
    return html


def svg_vo2max(activities):
    history = []
    ts = 0
    values = [a['vO2MaxValue'] for a in sorted(activities, key=lambda x: x['activityId']) if a['startTimeGMT'].startswith('%d' % CURRENT_YEAR)]
    for value in values:
        if value is not None:
            history.append(','.join([str(ts), str(200 - (value * 4))]))
            ts += 1

    svg = """
    <svg class="w-full" viewBox="0 0 200 50">
      <polyline fill="none" stroke="#000000" stroke-width="1" points="%s"/>
    </svg>
    """ % ('\n'.join(history))
    return svg


def svg_hr(activity):
    activity_start_date = dparser.parse(activity['startTimeGMT'])
    heart_ts_start = int((activity_start_date - timedelta(seconds=60) + timedelta(hours=1)).timestamp()) * 1000
    heart_ts_end = int(heart_ts_start + (activity['duration']*1000) + (3600 * 3
        * 1000))

    ts = activity['startTimeGMT'][0:10]

    workout_width = 100
    workout_x = 0

    with open("../%s/heart.dat" % ts) as json_file:
        data = json.load(json_file)
        beats = []
        ts = 0
        for row in data['heartRateValues']:
            if workout_x == 0 and row[0] >= (heart_ts_start + 3600000):
                workout_x = ts
                workout_width = int((activity['duration']+240)/60)

            if int(row[0]) >= heart_ts_start and int(row[0]) <= heart_ts_end:
                ts += 2

                bpm = row[1] or 200
                pm = 200 - bpm
                beats.append(','.join([str(ts), str(pm)]))

    svg = """
    <svg class="w-full" viewBox="0 0 400 200">
      <rect x="%s" width="%s" y="30" height="120" style="fill:rgb(237,249,255);stroke-width:0;" />
      <polyline fill="none" stroke="#000000" stroke-width="1" points="%s"/>
    </svg>
    """ % (workout_x, workout_width, '\n'.join(beats))

    return svg

distance_running = summary(activities, 'running', 'distance') / 1000
distance_walking = summary(activities, 'walking', 'distance') / 1000
distance_cycling = summary(activities, 'cycling', 'distance') / 1000

distance_running_this_year = summary_this_year(activities, 'running', 'distance') / 1000
distance_walking_this_year = summary_this_year(activities, 'walking', 'distance') / 1000
distance_cycling_this_year = summary_this_year(activities, 'cycling', 'distance') / 1000

duration_running = summary(activities, 'running', 'duration') / 3600
duration_walking = summary(activities, 'walking', 'duration') / 3600
duration_cycling = summary(activities, 'cycling', 'duration') / 3600
duration_strength = summary(activities, 'indoor_cardio', 'duration') / 3600

duration_running_this_year = summary_this_year(activities, 'running', 'duration') / 3600
duration_walking_this_year = summary_this_year(activities, 'walking', 'duration') / 3600
duration_cycling_this_year = summary_this_year(activities, 'cycling', 'duration') / 3600
duration_strength_this_year = summary_this_year(activities, 'indoor_cardio', 'duration') / 3600

duration_all_this_year = duration_running_this_year + duration_walking_this_year + duration_cycling_this_year + duration_strength_this_year 

distance_all_this_year = distance_walking_this_year + distance_cycling_this_year + distance_running_this_year

duration_all = duration_running + duration_walking + duration_cycling + duration_strength 

distance_all = distance_walking + distance_cycling + distance_running

active_days = distinct_active_days(activities)
d0 = date(CURRENT_YEAR, 1, 1)
d1 = date.today()
days_this_year = (d1 - d0).days
percentage_active_days = (active_days * 100) / days_this_year

component_groups = [
        {'name': 'activities', 'components': [
            {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%.2f km' % distance_all_this_year},
            {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % duration_all_this_year},
            {'label': 'Distance (total)', 'value': '%.2f km' % distance_all},
            {'label': 'Duration (total)', 'value': '%d h' % duration_all},
            {'label': 'Active days (%d)' % CURRENT_YEAR, 'value': '%d/%d (%d%%)' %
                (active_days, days_this_year, percentage_active_days)},
            {'label': 'VO2Max (%d)' % CURRENT_YEAR, 'value': vo2_max_widget(activities)}
            ]},
        {'name': 'running', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%.2f km' % (distance_running_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_running_this_year)},
        {'label': 'Distance (total)', 'value': '%.2f km' % (distance_running)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_running)},
        {'label': 'Last run HR', 'value': svg_hr(most_recent(activities,
            'running'))},
        {'label': 'Last track', 'value': svg_gpx(most_recent(activities,
            'running'))},
        {'label': 'Longest run', 'value': '%.2f km' % (maximum(activities, 'running', 'distance') / 1000.00)}

        ]},

        {'name': 'strength', 'components': [
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_strength_this_year)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_strength)},
        {'label': 'Last workout HR', 'value': svg_hr(most_recent(activities,
            'indoor_cardio'))},
        ]},

        {'name': 'cycling', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%.2f km' % (distance_cycling_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_cycling_this_year)},
        {'label': 'Distance (total)', 'value': '%.2f km' % (distance_cycling)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_cycling)},
        {'label': 'Last cycle HR', 'value': svg_hr(most_recent(activities,
            'cycling'))},
        {'label': 'Last track', 'value': svg_gpx(most_recent(activities,
            'cycling'))}
        ]},

        {'name': 'walking', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%.2f km' % (distance_walking_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_walking_this_year)},
        {'label': 'Distance (total)', 'value': '%.2f km' % (distance_walking)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_walking)},
        {'label': 'Last walk HR', 'value': svg_hr(most_recent(activities,
            'walking'))},
        {'label': 'Last track', 'value': svg_gpx(most_recent(activities,
            'walking'))}
        ]},
]

base_html = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link href="dist/tailwind.css" rel="stylesheet">
</head>
<body>

  <img class="w-36 max-w-48 lg:w-48 inline p-2 font-bold" src="dist/fig1.svg"/>

  ${groups}

  <footer class="p-6 bg-black text-gray-300 border rounded">
    <p class="text-xs"><a href="https://github.com/aerosol/me"
    class="underline">Code</a> &amp; 
    data: <a class="underline" href="https://twitter.com/itshq1">hq1</a> 
    | symbol: <a href="https://twitter.com/Biernacki" class="underline">Biernacki</a></p>
    <p class="text-xs">Made with: 
    <a class="underline" href="https://tailwindcss.com/">tailwindcss</a> (MIT), 
    <a class="underline" href="https://gitlab.com/l3u/gpx2svg/">gpx2svg</a> (GPL3), 
    <a class="underline" href="https://github.com/cyberjunky/python-garminconnect">garminconnect</a> (MIT)</p>
  </footer>

</body>
</html>
"""

group_html = """
  <div class="flex items-stretch">
    <h1 class="w-36 max-w-48 lg:w-48 bg-gray-100 rounded text-gray-500 inline m-2 p-2 font-bold text-center">${caption}</h1>
    <div class="max-w-7xl w-full mx-auto py-6 px-2">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            ${components}
        </div>
    </div>
  </div>
  <hr/>
"""

component_html = """
            <div class="w-full pr-4">
                <div class="widget w-full p-4 rounded-lg bg-white dark:bg-gray-900 dark:border-gray-800 align-middle">
                    <div class="flex flex-row items-stretch">
                        <div class="flex flex-col items-stretch">
                            <div class="text-gray-500 align-middle">
                                ${label}
                            </div>
                            <div class="text-xl font-bold align-middle">
                                ${value}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
"""

base = string.Template(base_html)


groups = ''
for group in component_groups:
    components = ''
    group_tpl = string.Template(group_html)

    for data in group['components']:
        component = string.Template(component_html)
        components += component.substitute(data)

    groups += group_tpl.substitute(components=components, caption=group['name'])

render = base.substitute(groups=groups)

print(render)
