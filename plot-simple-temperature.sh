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
set ytics 1
set ylabel "Temperature (C)"
set link y2
set y2tics 1

set term svg size 768,480
plot "$FILE1" using 1:2 with lines title "$FILE1_TITLE", \
     "$FILE2" using 1:2 with lines title "$FILE2_TITLE"
EOF
