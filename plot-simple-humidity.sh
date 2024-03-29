#!/bin/sh

if [ -z "$1" -o -z "$2" ]; then
    echo "usage: $0 <FILE1> <FILE2>" >&2
    exit 1
fi

FILE1="$1"
FILE2="$2"

FILE1_TITLE="Inside"
FILE2_TITLE="Outside"

gnuplot <<EOF
set xdata time
set timefmt "%Y%m%dT%H%M%S"
set format x "%H:%M"
set grid
set ylabel "Humidity (%)"
set link y2
set y2tics

set term svg size 768,480
plot "$FILE1" using 1:3 with lines title "$FILE1_TITLE", \
     "$FILE2" using 1:3 with lines title "$FILE2_TITLE"
EOF
