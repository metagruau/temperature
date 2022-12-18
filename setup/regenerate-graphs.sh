#!/bin/sh

set -e
set -u
set -x

ROOT_WWW="/home/pi/www"

mkdir -p $ROOT_WWW/archives
mkdir -p $ROOT_WWW/archives-weekly-inside

while true; do
    DATE_MIN=$(date -d 'yesterday' +%Y%m%dT0000)

    cd /home/pi/observations
    extract-data.py --date-min "$DATE_MIN" < inside.txt > last-day-inside.txt
    extract-data.py --date-min "$DATE_MIN" < CWQB.txt > last-day-CWQB.txt
    if [ -s last-day-inside.txt -o -s last-day-CWQB.txt ]; then
	plot-simple-temperature.sh last-day-inside.txt last-day-CWQB.txt > $ROOT_WWW/last-day-temperature.svg
	plot-simple-humidity.sh last-day-inside.txt last-day-CWQB.txt > $ROOT_WWW/last-day-humidity.svg
    fi

    # graph inside temperatures over the current week
    WEEK_MIN=$(date -d 'last saturday + 1 day' +%Y%m%d)
    WEEK_MAX=$(date -d "$WEEK_MIN + 7 days" +%Y%m%d)
    extract-data.py --date-min "${WEEK_MIN}T0000" --date-max "${WEEK_MAX}T0000" < inside.txt \
        | map-to-daily-data-set.awk > last-week-inside.txt
    if [ -s last-week-inside.txt ]; then
	plot-7days-temperature.sh last-week-inside.txt "$WEEK_MIN - $WEEK_MAX" > $ROOT_WWW/last-week-inside-temperature.svg
	cp $ROOT_WWW/last-week-inside-temperature.svg $ROOT_WWW/archives-weekly-inside/$WEEK_MIN.svg
    fi

    YESTERDAY=$(date -d 'yesterday' +%Y%m%d)
    if [ ! -f "$ROOT_WWW/archives/$YESTERDAY-temperature.svg" ]; then
        DATE_MIN=$(date -d 'yesterday' +%Y%m%dT0000)
        DATE_MAX=$(date +%Y%m%dT0000)
        extract-data.py --date-min "$DATE_MIN" --date-max "$DATE_MAX" < inside.txt > yesterday-inside.txt
        extract-data.py --date-min "$DATE_MIN" --date-max "$DATE_MAX" < CWQB.txt > yesterday-CWQB.txt

        plot-simple-temperature.sh yesterday-inside.txt yesterday-CWQB.txt > $ROOT_WWW/archives/$YESTERDAY-temperature.svg
        plot-simple-humidity.sh yesterday-inside.txt yesterday-CWQB.txt > $ROOT_WWW/archives/$YESTERDAY-humidity.svg
    fi

    sleep 10m
done
