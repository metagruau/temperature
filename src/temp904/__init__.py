import dataclasses
import time


# XXX p-e qu'on devrait avoir quelques moyens d'en créer, et quelques méthodes pour faciliter
#     les conversions; ou p-e un espece de builder
@dataclasses.dataclass
class Observation:
    time: int  # Unix time (epoch)
    temperature: float | None  # in Celsius
    humidity: float | int | None  # relative humidity percentage, between 0 and 100

    @classmethod
    def now(cls, temperature, humidity):
        return cls(int(time.time()), temperature, humidity)
