#!/bin/awk -f

# Transform an observations input stream with multiple data points
# per day to an output stream with a single line per day in
# format "20220102 21.1 23.2" (<date> <min temp> <max temp>)

BEGIN {
	cur_max = 0.0
	cur_min = 100.0
	cur_date = ""
}

{
	date = substr($1, 1, 8)
	value = $2
	if (cur_date != date) {
		if (cur_date != "") {
			print cur_date, cur_min, cur_max
		}
		cur_date = date
		cur_max = value
		cur_min = value
	} else if (value > cur_max) {
		cur_max = value
	} else if (value < cur_min) {
		cur_min = value
	}
}

END {
	print cur_date, cur_min, cur_max
}
