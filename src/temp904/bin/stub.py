from temp904.bin import common
from temp904.probes.stub import StubProbe


def main():
    cfg = _parse_args()
    common.setup(cfg)

    probe = StubProbe(cfg.target_temperature, cfg.target_humidity)
    common.run(cfg, probe)


def _parse_args():
    parser = common.new_arg_parser()
    parser.add_argument("--target-temperature", default=20.0, type=float)
    parser.add_argument("--target-humidity", default=45.0, type=float)
    return parser.parse_args()


if __name__ == "__main__":
    main()
