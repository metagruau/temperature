#!/bin/sh

mkdir -p /home/pi/observations

read-temp-dht22.py --interval 600 | tee -a /home/pi/observations/inside.txt
