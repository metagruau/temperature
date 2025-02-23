from temp904.bin import common
from temp904.probes.ds18b20 import DS18B20Probe


def main():
    cfg = _parse_args()
    common.setup(cfg)

    probe = DS18B20Probe(cfg.w1_slave_path)
    common.run(cfg, probe)


def _parse_args():
    parser = common.new_arg_parser()
    parser.add_argument("--w1-slave-path", help="path to w1-slave sensor file")
    return parser.parse_args()


if __name__ == "__main__":
    main()
