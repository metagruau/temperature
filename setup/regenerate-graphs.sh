#!/bin/sh

set -e
set -x

mkdir -p /home/pi/www/archives

while sleep 10m; do
    DATE_MIN=$(date -d 'yesterday' +%Y%m%dT0000)

    cd /home/pi/observations
    extract-data.py --date-min "$DATE_MIN" < inside.txt > last-day-inside.txt
    extract-data.py --date-min "$DATE_MIN" < CWQB.txt > last-day-CWQB.txt
    plot-simple-temperature.sh last-day-inside.txt last-day-CWQB.txt > /home/pi/www/last-day-temperature.svg
    plot-simple-humidity.sh last-day-inside.txt last-day-CWQB.txt > /home/pi/www/last-day-humidity.svg

    YESTERDAY=$(date -d 'yesterday' +%Y%m%d)
    if [ ! -f "/home/pi/www/archives/$YESTERDAY-temperature.svg" ]; then
	DATE_MIN=$(date -d 'yesterday' +%Y%m%dT0000)
	DATE_MAX=$(date +%Y%m%dT0000)
	extract-data.py --date-min "$DATE_MIN" --date-max "$DATE_MAX" < inside.txt > yesterday-inside.txt
	extract-data.py --date-min "$DATE_MIN" --date-max "$DATE_MAX" < CWQB.txt > yesterday-CWQB.txt
	plot-simple-temperature.sh yesterday-inside.txt yesterday-CWQB.txt > /home/pi/www/archives/$YESTERDAY-temperature.svg
	plot-simple-humidity.sh yesterday-inside.txt yesterday-CWQB.txt > /home/pi/www/archives/$YESTERDAY-humidity.svg
    fi
done
