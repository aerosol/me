#!/usr/bin/env python3

import json
import os
import sys
import glob

activities = []

for name in glob.glob('_activities/*.json'):
    with open(name, 'r') as activity:
        obj = json.loads(activity.read())
        activities.append(obj)

def summary(activities, activity_type, field):
    return sum(a[field] for a in activities if a['activityType']['typeKey'] == activity_type)

def summary_this_year(activities, activity_type, field):
    this_year = [a for a in activities if a['startTimeGMT'].startswith('2021')]
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

print('Distance running: %d km (%d km this year)' % (distance_running, distance_running_this_year))
print('Distance walking: %d km (%d km this year)' % (distance_walking, distance_walking_this_year)) 
print('Distance cycling: %d km (%d km this year)' % (distance_cycling, distance_cycling_this_year))

print('Duration running: %d h (%d h this year)' % (duration_running, duration_running_this_year))
print('Duration walking: %d h (%d h this year)' % (duration_walking, duration_walking_this_year))
print('Duration cycling: %d h (%d h this year)' % (duration_cycling, duration_cycling_this_year))
