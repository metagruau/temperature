#!/bin/sh

if [ -z "$1" -o -z "$2" ]; then
    echo "usage: $0 <FILE1> <YEAR>" >&2
    exit 1
fi

FILE1="$1"
YEAR="$2"

gnuplot <<EOF
set xdata time
set timefmt "%Y%m%d"
set format x "%b"
set xrange ["${YEAR}0101":"${YEAR}1231"]
set grid
set ytics 1
set ylabel "Temperature (C)"
set link y2
set y2tics 1
set xlabel "$YEAR"

set term svg size 768,480
plot "$FILE1" using 1:2 with lines title "Min", \
     "$FILE1" using 1:3 with lines title "Max"
EOF
