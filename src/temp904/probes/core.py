# XXX singular or plural class names ?
# XXX temperature -> temp ? humidity -> hmdt ?

import dataclasses

from temp904 import Observation


@dataclasses.dataclass
class ProbeCapabilities:
    has_temperature: bool  # true if probe can read temperature
    has_humidity: bool     # true if probe can read humidity
    min_interval: float    # in seconds


# XXX experimentation
class ProbeConfig:
    get_temperature: bool  # true if we want to observe temperature
    get_humidity: bool


# XXX interface... not used anywhere currently
class AbstractProbe:
    capabilities: ProbeCapabilities  # XXX or staticmethod, maybe it should go in a factory tho

    def close(self):
        pass

    def __enter__(self):
        # TODO do any late initialization stuff, for example connect to the DB ? or should that be done
        #      when the Probe is created ?
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def observe(self) -> Observation:
        return NotImplementedError()
