import logging
import os

from temp904 import Observation
from .core import ProbeCapabilities

logger = logging.getLogger(__name__)


class DS18B20Probe:
    _W1_DEVICES_PATH = "/sys/bus/w1/devices"

    capabilities = ProbeCapabilities(
        has_temperature=True,
        has_humidity=False,
        min_interval=2.0,  # XXX we don't know
    )

    def __init__(self, w1_slave_path=None):
        if w1_slave_path is None:
            for filename in os.listdir(self._W1_DEVICES_PATH):
                if filename.startswith("28-"):
                    self._path = os.path.join(self._W1_DEVICES_PATH, filename, "w1_slave")
                    logger.info("Found DS18B20 sensor at %s", self._path)
                    break
            else:
                raise RuntimeError("no DS18B20 sensors found")
        else:
            self._path = w1_slave_path

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def observe(self):
        with open(self._path) as fobj:
            lines = fobj.readlines()
        temp_idx = lines[1].find("t=")
        if temp_idx == -1:
            raise RuntimeError(f"Failed to read temperature: could not find t= line in {self._path}")
        temp_str = lines[1][temp_idx+2:]
        temperature = float(temp_str) / 1000.0
        return Observation.now(temperature, None)

