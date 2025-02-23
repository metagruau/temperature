import logging

from collections import deque

from temp904 import Observation

logger = logging.getLogger(__name__)

# XXX name is not good, should emphasis that it does nothing when everything is ok
class BufferStorage:

    def __init__(self, storage, path, limit=1000):
        self._storage = storage
        # XXX there's a risk we are storing invalid observation (bug) and that we are
        #     "poisoning" the cache that way, maybe we should validate observations ?
        self._buffer = deque(maxlen=limit)
        self._load(path)

    def _load(self, path):
        try:
            self._fobj = open(path, "r+")
        except FileNotFoundError:
            self._fobj = open(path, "w+")
        for line in self._fobj:
            ts, temperature, humidity = line.rstrip("\n").split("\t")[:3]
            ts = int(ts)
            temperature = float(temperature) if temperature else None
            humidity = float(humidity) if humidity else None
            self._buffer.append(Observation(ts, temperature, humidity))
        logger.info("Loaded %s observations from buffer file", len(self._buffer))

    def _save(self):
        self._fobj.truncate(0)
        self._fobj.seek(0)
        for observation in self._buffer:
            self._fobj.write(self._serialize_observation(observation))
        self._fobj.flush()

    def _save_append(self, observation):
        self._fobj.write(self._serialize_observation(observation))
        self._fobj.flush()

    @staticmethod
    def _serialize_observation(observation):
        temperature = "" if observation.temperature is None else observation.temperature
        humidity = "" if observation.humidity is None else observation.humidity
        return f"{observation.time}\t{temperature}\t{humidity}\n"

    def close(self):
        self._storage.close()
        self._fobj.close()

    def store(self, observation):
        if not self._buffer:
            # fast path
            try:
                self._storage.store(observation)
            except Exception:
                self._buffer.append(observation)
                self._save_append(observation)
                raise
        else:
            # slow path, try to insert them in order since not all storage support not-in-order
            # TODO use store_many
            self._buffer.append(observation)
            stored_one = False
            try:
                while self._buffer:
                    self._storage.store(self._buffer[0])
                    self._buffer.popleft()
                    stored_one = True
            except Exception:
                if stored_one:
                    self._save()
                else:
                    self._save_append(observation)
                raise
            else:
                self._save()

    def store_many(self, observations):
        # TODO
        raise NotImplementedError()

    def __enter__(self):
        # XXX faudrait prob appeler __enter__ de self._storage mais est-ce que y a une facon pas hackish de le faire ? ou est
        #     ce que c'est nous qui pensons que c'est hackish masi ca ne l'est pas ? dans tous les cas, ca smell, là présentement
        #     ca suppose que __enter__ fait rien pour aucun des storage
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
