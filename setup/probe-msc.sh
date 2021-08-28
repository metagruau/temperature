#!/bin/sh

mkdir -p /home/pi/observations

read-temp-msc | tee -a /home/pi/observations/CWQB.txt
