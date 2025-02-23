from temp904 import Observation
from .core import ProbeCapabilities


class StubProbe:
    capabilities = ProbeCapabilities(
        has_temperature=True,
        has_humidity=True,
        min_interval=0.0,
    )

    def __init__(self, target_temperature=20.0, target_humidity=45.0):
        self._base_temperature = target_temperature - 0.5
        self._base_humidity = max(target_humidity - 5, 0.0)
        self._offset = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def observe(self):
        temperature = self._base_temperature + self._offset * 0.1
        humidity = min(self._base_humidity + self._offset, 100.0)
        obs = Observation.now(temperature, humidity)
        self._offset = (self._offset + 1) % 10
        return obs
