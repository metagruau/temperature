#!/usr/bin/env python3

import argparse
import datetime
import sys

# XXX we're using more than one date format (one for arg, one for parsing), name is confusing
#     this one is the date format used in the standard text file
DATEFMT = "%Y%m%dT%H%M%S"


def main():
    cfg = _parse_args()

    if cfg.date_min:
        dt_min = cfg.date_min
    else:
        dt_min = datetime.datetime.now() - datetime.timedelta(hours=24)
    if cfg.date_max:
        dt_max = cfg.date_max
    else:
        dt_max = datetime.datetime.now()

    _extract_datapoints(sys.stdin, sys.stdout, dt_min, dt_max)


def _parse_args():
    parser = argparse.ArgumentParser()
    # TODO actually implement UTC support kek, or remove it everywhere
    parser.add_argument("-u", "--utc", action="store_true", help="format time in UTC")
    parser.add_argument("--date-min", type=_cli_date, help="in format YYYYMMDDThhmm")
    parser.add_argument("--date-max", type=_cli_date, help="in format YYYYMMDDThhmm")
    return parser.parse_args()


def _cli_date(value):
    return datetime.datetime.strptime(value, "%Y%m%dT%H%M")


def _extract_datapoints(fobj_in, fobj_out, dt_min, dt_max):
    textual_min = dt_min.strftime(DATEFMT)
    textual_max = dt_max.strftime(DATEFMT)
    l = len(textual_min)

    # find first line matching dt_min
    for line in fobj_in:
        # ignore invalid lines, by checking if the first 8 characters are all digits
        if not line[:8].isdigit():
            continue

        if line[:l] >= textual_min:
            break
    else:
        # read the whole file without finding any date earlier than dt_min
        return

    fobj_out.write(line)
    # find last line matching dt_max
    for line in fobj_in:
        # ignore invalid lines, by checking if the first 8 characters are all digits
        if not line[:8].isdigit():
            continue

        if line[:l] < textual_max:
            fobj_out.write(line)
        else:
            break


if __name__ == "__main__":
    main()
