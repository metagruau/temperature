import argparse
import logging
import signal
import sys
import time

logger = logging.getLogger()


def new_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--interval", default=10.0, type=float, help="sampling interval in seconds")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--temperature-delta", default=0.0, type=float, help="delta to add to temperature")
    parser.add_argument("--temperature-round", type=int, help="round temperature to this number of decimal")
    parser.add_argument("--local-buffer", help="file to store observation locally in case of storage failure")
    # TODO implement eventually
    parser.add_argument("--no-humidity", action="store_true", help="do not measure humidity")
    # storage
    parser.add_argument("-s", "--storage", default="text", choices=["postgres", "text"], help="storage backend")
    parser.add_argument("--postgres-conninfo", help="postgres connection string")
    parser.add_argument("--postgres-source-id", help="sensor source id")
    parser.add_argument("--text-output", help="write output to file instead of stdout")
    parser.add_argument("--text-utc", action="store_true", help="format time in UTC")
    return parser


def setup(cfg):
    level = logging.DEBUG if cfg.verbose else logging.INFO
    logging.basicConfig(format="%(asctime)s %(message)s", level=level)

    logger.debug("Config: %s", cfg)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)


def _handle_signal(signum, frame):
    raise SystemExit(0)


def run(cfg, probe):
    # XXX maybe storage instantiation should be done earlier, to validate args
    storage = _new_storage(cfg)
    interval = max(probe.capabilities.min_interval, cfg.interval)
    logger.debug("Sampling interval: %s", interval)
    with probe, storage:
        while True:
            try:
                obs = probe.observe()
            except Exception:
                # XXX ideally we would catch a less generic exception
                logger.exception("Failed to get observation")
            else:
                logger.debug("Got observation %s", obs)
                obs.temperature += cfg.temperature_delta
                if cfg.temperature_round:
                    obs.temperature = round(obs.temperature, cfg.temperature_round)
                logger.debug("Adjusted observation %s", obs)
                try:
                    storage.store(obs)
                except Exception:
                    # XXX ideally we would catch a less generic exception
                    logger.exception("Failed to store observation:")
                else:
                    logger.debug("Successfully stored observation")

            # XXX given that sampling can be slow, this can lead to some drift in the sampling interval
            time.sleep(interval)


def _new_storage(cfg):
    match cfg.storage:
        case "text":
            from temp904.storage.text import TextFileStorage
            if cfg.text_output:
                raise NotImplementedError("only writing to stdout is supported")
            storage = TextFileStorage(sys.stdout, utc=bool(cfg.text_utc))
        case "postgres":
            from temp904.storage.postgres import PostgresStorage
            if not cfg.postgres_conninfo:
                raise Exception("conninfo required when using postgres backend")
            storage = PostgresStorage(cfg.postgres_conninfo, cfg.postgres_source_id)
        case _:
            raise Exception("invalid storage name %s", cfg.storage)
    if cfg.local_buffer:
        from temp904.storage.buffer import BufferStorage
        storage = BufferStorage(storage, cfg.local_buffer)
    return storage
