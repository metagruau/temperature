from temp904.bin import common
from temp904.probes.msc import MSCDatamartProbe


def main():
    cfg = _parse_args()
    common.setup(cfg)

    probe = MSCDatamartProbe.new_station_quebec()
    common.run(cfg, probe)


def _parse_args():
    parser = common.new_arg_parser()
    # TODO add a way to configure which station to read from
    return parser.parse_args()


if __name__ == "__main__":
    main()
