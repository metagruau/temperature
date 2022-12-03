#!/bin/awk -f

BEGIN {
	cur_date = ""
}

{
	date = substr($1, 1, 8)
	time = substr($1, 10, 6)
	if (cur_date != date) {
		if (cur_date != "") {
			# print two blank lines (gnu plot "multi-data-set" file format)
			print ""
			print ""
		}
		cur_date = date
	}

	print date, time, $2, $3
}
