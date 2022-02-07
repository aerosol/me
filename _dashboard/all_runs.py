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
            <img class="h-64" src="%s"/>
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

    <h1 class="w-36 max-w-48 lg:w-48 bg-black text-white m-6 p-6 font-bold text-center">ALL-RUNS</h1>

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
<div class="grid grid-cols-4 gap-4 p-10">
  ${components}
</div>
"""

component_html = """
  <div class="relative">
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <span class="bg-black text-white p-4 opacity-75 border-white border-4">${distance}km ${time}min</span>
    </div>
    ${gpx}
  </div>
"""

base = string.Template(base_html)
components = ''

for activity in all_runs(activities):
    group_tpl = string.Template(group_html)

    component = string.Template(component_html)
    (distance, gpx) = svg_gpx(activity)
    duration = round(activity['duration'] / 60)
    components += component.substitute(gpx=gpx,
            distance=distance, time=duration)

groups = group_tpl.substitute(components=components)
render = base.substitute(groups=groups)

print(render)
