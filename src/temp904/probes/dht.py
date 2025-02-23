from temp904 import Observation
from .core import ProbeCapabilities


class DHTProbe:
    capabilities = ProbeCapabilities(
        has_temperature=True,
        has_humidity=True,
        min_interval=2.0,
    )

    def __init__(self, dht_device):
        # take ownership of dht_device
        self._dht_device = dht_device

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._dht_device.exit()
        return False

    def observe(self):
        while True:
            try:
                temperature = self._dht_device.temperature
                humidity = self._dht_device.humidity
            except RuntimeError as e:
                logger.debug("Failed to read DHT22: %s", e)
                time.sleep(2)
            else:
                return Observation.now(temperature, humidity)
