#!/bin/sh

if [ -z "$1" -o -z "$2" ]; then
    echo "usage: $0 <FILE1> <XLABEL> [<TITLES>]" >&2
    exit 1
fi

FILE1="$1"
XLABEL="$2"
#TITLES="${3:-Su M Tu W Th F Sa}"
TITLES="${3:-D L Ma Me J V S}"

gnuplot <<EOF
set xdata time
set timefmt "%H%M%S"
set format x "%H:%M"
set grid
set ytics 1
set ylabel "Temperature (C)"
set xlabel "$XLABEL"
set key horizontal

titles="$TITLES"

set term svg size 768,480
plot for [i=0:*] "$FILE1" index i using 2:3 with lines title word(titles,i+1)
EOF
