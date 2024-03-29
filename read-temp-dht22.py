#!/usr/bin/env python3

import adafruit_dht
import board

import argparse
import dataclasses
import datetime
import logging
import signal
import sys
import time

logger = logging.getLogger()

DATEFMT = "%Y%m%dT%H%M%S"


@dataclasses.dataclass
class Observation:
    time: int  # Unix time (epoch)
    temperature: float  # in Celsius
    humidity: int  # relative humidity percentage, between 0 and 100


def main():
    cfg = _parse_args()
    _setup_logging(cfg)
    logger.debug("Config: %s", cfg)

    signal.signal(signal.SIGTERM, _handle_signal)

    interval = max(cfg.interval, 2.0)
    dht_device = adafruit_dht.DHT22(cfg.pin)
    try:
        probe = DHTProbe(dht_device)
        storage = TextFileStorage(sys.stdout, cfg.utc)
        while True:
            obs = probe.observe()
            storage.store(obs)

            # XXX given that sampling on DHT is error prone and slow, this can
            #     lead to some drift in the sampling interval
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        dht_device.exit()


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", default=10.0, type=float, help="sampling interval in seconds")
    parser.add_argument("-u", "--utc", action="store_true", help="format time in UTC")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--pin", default="D4", type=_pin, help="pin name")
    return parser.parse_args()


def _pin(value):
    try:
        return getattr(board, value)
    except AttributeError:
        raise ValueError("unknown pin value {}".format(value))


def _setup_logging(cfg):
    level = logging.DEBUG if cfg.verbose else logging.INFO
    logging.basicConfig(format="%(asctime)s %(message)s", level=level)


def _handle_signal(signum, frame):
    raise SystemExit(1)


class DHTProbe:

    def __init__(self, dht_device):
        self._dht_device = dht_device

    def observe(self):
        while True:
            try:
                temperature = self._dht_device.temperature
                humidity = self._dht_device.humidity
            except RuntimeError as e:
                logger.debug("Failed to read DHT22: %s", e)
                time.sleep(2)
            else:
                return Observation(int(time.time()), temperature, round(humidity))


class TextFileStorage:

    def __init__(self, fobj, utc=False):
        self._fobj = fobj
        self._tz = datetime.timezone.utc if utc else None

    def store(self, obs):
        print(self._format(obs), file=self._fobj)
        self._fobj.flush()

    def _format(self, obs):
        dt = datetime.datetime.fromtimestamp(obs.time, tz=self._tz)
        fmt_dt = dt.strftime(DATEFMT)
        return "{}\t{:.1f}\t{}".format(fmt_dt, obs.temperature, obs.humidity)


if __name__ == "__main__":
    main()
