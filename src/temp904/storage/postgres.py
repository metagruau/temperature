import psycopg
import psycopg.errors

import datetime
import logging

logger = logging.getLogger(__name__)


class PostgresStorage:

    def __init__(self, conninfo, source_id=None):
        self._conninfo = conninfo
        self._orig_source_id = source_id
        self._conn = None
        self._source_id = source_id

    def close(self):
        self._reset_conn()

    def store(self, observation):
        ts = datetime.datetime.utcfromtimestamp(observation.time)
        try_count = 0
        while True:
            try:
                self._maybe_conn()
                with self._conn.cursor() as cur:
                    # TODO use a view instead
                    if observation.temperature:
                        cur.execute("INSERT INTO temp_observations (ts, source_id, value) VALUES (%s, %s, %s)",
                                    (ts, self._source_id, observation.temperature))
                    if observation.humidity:
                        cur.execute("INSERT INTO hmdt_observations (ts, source_id, value) VALUES (%s, %s, %s)",
                                    (ts, self._source_id, observation.humidity))
                break
            except psycopg.errors.Error as e:
                logger.error("Failed to insert observation to postgres: %s", e)
                self._reset_conn()
                if try_count >= 1:
                    raise
                try_count += 1

    def store_many(self, observations):
        raise NotImplementedError()

    def _maybe_conn(self):
        if self._conn:
            return

        self._conn = psycopg.connect(self._conninfo, autocommit=True)
        logger.info("Connected to postgres server")
        with self._conn.cursor() as cur:
            cur.execute("SET timezone to 'Etc/UTC'")
            if self._orig_source_id is None:
                cur.execute("SELECT source_id FROM user_source_map WHERE username = current_user")
                record = cur.fetchone()
                if record is None:
                    raise Exception("no source_id specified and no default source configured on server")
                self._source_id = record[0]
                logger.info("Found default source ID %s", self._source_id)

    def _reset_conn(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        return False
