#!/usr/bin/env bash
mkdir -p sqlite-input
./process.py
sqlite-utils insert me.db steps sqlite-input/steps.json --ignore --pk=id
sqlite-utils insert me.db daily_sleep sqlite-input/daily_sleep_data.json --ignore --pk=id
sqlite-utils insert me.db heart_rates sqlite-input/heart_rates.json --ignore --pk=id
sqlite-utils insert me.db respirations sqlite-input/respirations.json --ignore --pk=id
sqlite-utils insert me.db sleep_movements sqlite-input/sleep_movements.json --ignore --pk=id
sqlite-utils insert me.db sleep_activity_levels sqlite-input/sleep_activity_levels.json --ignore --pk=id
