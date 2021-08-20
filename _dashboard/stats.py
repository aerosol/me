#!/usr/bin/env python3

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

def summary(activities, activity_type, field):
    return sum(a[field] for a in activities if a['activityType']['typeKey'] == activity_type)

def summary_this_year(activities, activity_type, field):
    this_year = [a for a in activities if a['startTimeGMT'].startswith('%d' %
        CURRENT_YEAR)]
    return summary(this_year, activity_type, field)

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

def most_recent(activities, activity_type):
    return [a for a in sorted(activities, key=lambda x: x['activityId']) if a['activityType']['typeKey'] ==
            activity_type][-1]

def svg_gpx(activity):
    return '<img src="dist/_activities-svg/activity_%s.gpx.svg"/>' % activity['activityId']

def svg_hr(activity):
    ts = activity['startTimeGMT'][0:10]

    with open("../%s/heart.dat" % ts) as json_file:
        data = json.load(json_file)
        beats = []
        ts = 10
        for row in data['heartRateValues']:
            ts += 1
            pm = 200 - row[1]
            beats.append(','.join([str(ts), str(pm)]))

    svg = """
    <svg viewBox="0 0 500 200" class="chart">
      <polyline
         fill="none"
         stroke="#000000"
         stroke-width="1"
         points="
         %s
         "/>
    </svg>
    """ % ('\n'.join(beats))

    return svg

component_groups = [
        {'name': 'Running', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%d km' % (distance_running_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_running_this_year)},
        {'label': 'Distance (total)', 'value': '%d km' % (distance_running)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_running)},
        {'label': 'Last HR', 'value': svg_hr(most_recent(activities,
            'running'))},
        {'label': 'Last track', 'value': svg_gpx(most_recent(activities,
            'running'))}

        ]},

        {'name': 'Strength', 'components': [
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_strength_this_year)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_strength)},
        {'label': 'Last HR', 'value': svg_hr(most_recent(activities,
            'indoor_cardio'))},
        ]},

        {'name': 'Cycling', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%d km' % (distance_cycling_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_cycling_this_year)},
        {'label': 'Distance (total)', 'value': '%d km' % (distance_cycling)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_cycling)},
        {'label': 'Last HR', 'value': svg_hr(most_recent(activities,
            'cycling'))},
        {'label': 'Last track', 'value': svg_gpx(most_recent(activities,
            'cycling'))}
        ]},

        {'name': 'Walking', 'components': [
        {'label': 'Distance (%d)' % CURRENT_YEAR, 'value': '%d km' % (distance_walking_this_year )},
        {'label': 'Duration (%d)' % CURRENT_YEAR, 'value': '%d h' % (duration_walking_this_year)},
        {'label': 'Distance (total)', 'value': '%d km' % (distance_walking)},
        {'label': 'Duration (total)', 'value': '%d h' % (duration_walking)},
        {'label': 'Last HR', 'value': svg_hr(most_recent(activities,
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

  ${groups}

</body>
</html>
"""

group_html = """
  <div class="flex items-stretch">
    <h1 class="text-4xl w-96 bg-black text-white inline p-8 font-bold">${caption}</h1>
    <div class="max-w-7xl w-full mx-auto py-6 sm:px-6 lg:px-8">
        <div class="grid grid-cols-2 gap-2">
            ${components}
        </div>
    </div>
  </div>
  <hr/>
"""

component_html = """
            <div class="w-full">
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
