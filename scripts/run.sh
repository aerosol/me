#!/usr/bin/env bash

./plot_heart.py > /tmp/heart.csv
gnuplot ./heart.plot
