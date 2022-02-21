#!/usr/bin/env python3

from datetime import datetime
from datetime import timedelta
import json
import os
import sys
import glob
import string
from datetime import date
from pathlib import Path

CURRENT_YEAR = date.today().year

activities = []

for name in glob.glob('../_activities/*.json'):
    with open(name, 'r') as activity:
        obj = json.loads(activity.read())
        activities.append(obj)

def all_runs(activities):
    ax = sorted(activities, key=lambda x: x['activityId'], reverse=True)
    return [a for a in ax if a['activityType']['typeKey'] == 'running']

def svg_gpx(activity):
    distance = "%.2f" % (activity['distance'] / 1000)
    image = Path("dist/_activities-svg/activity_%s.gpx.svg" % activity['activityId'])
    if image.is_file():
        return (distance, """
            <div class="w-full flex justify-center"><img class="h-64" src="%s"/></div>
        """ % image)
    return (distance, "")

base_html = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link href="dist/tailwind.css" rel="stylesheet">
</head>
<body>

    <h1 class="w-36 max-w-48 lg:w-48 bg-black text-white m-6 p-6 font-bold text-center">Joglog</h1>

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

<div class="container mx-auto">
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
  ${components}
  </div>
</div>
"""

component_html = """
  <div class="flex justify-center p-2 mb-8 mt-8">
        <div class="block w-full mx-auto">${gpx}
            <div class="flex justify-between text-xs pt-2 border-t m-4">
              <div>🏃 ${distance}&nbsp;km</div>
              <div>⏱️  ${time}&nbsp;min</div>
              <div>🔥 ${calories}&nbsp;kcal</div>
            </div>
        </div>
  </div>
"""

base = string.Template(base_html)
components = ''

for activity in all_runs(activities):
    group_tpl = string.Template(group_html)

    component = string.Template(component_html)
    (distance, gpx) = svg_gpx(activity)
    calories = round(activity['calories'])
    duration = round(activity['duration'] / 60)
    components += component.substitute(gpx=gpx,
            distance=distance, time=duration, calories=calories)

groups = group_tpl.substitute(components=components)
render = base.substitute(groups=groups)

print(render)
