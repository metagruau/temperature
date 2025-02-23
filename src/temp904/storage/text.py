import datetime


class TextFileStorage:
    _DATEFMT = "%Y%m%dT%H%M%S"

    def __init__(self, fobj, utc=False):
        self._fobj = fobj
        self._tz = datetime.timezone.utc if utc else None

    def close(self):
        # no-op
        pass

    def store(self, observation):
        print(self._format(observation), file=self._fobj)
        self._fobj.flush()

    def store_many(self, observations):
        # XXX ca souleve la question de, si le storage n'est pas transactionelle et que ca échoue, comment le client
        #     fait pour savoir lesquels ont été inséré ou non. D'ailleurs aussi c'est un probleme un peu insoluble
        #     dans le sens que meme si c'est transactionelle, ca se peut que le data soit rééllement inséré meme 
        #     si on obtient ultimement une erreur
        try:
            for observation in observations:
                print(self._format(observation), file=self._fobj)
        finally:
            self._fobj.flush()

    def _format(self, observation):
        dt = datetime.datetime.fromtimestamp(observation.time, tz=self._tz)
        fmt_dt = dt.strftime(self._DATEFMT)
        fmt_temperature = "-" if observation.temperature is None else format(observation.temperature, ".1f")
        fmt_humidity = "-" if observation.humidity is None else format(round(observation.humidity))
        return "\t".join([fmt_dt, fmt_temperature, fmt_humidity])

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False
