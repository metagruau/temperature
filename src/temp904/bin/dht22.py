import adafruit_dht
import board

from temp904.bin import common
from temp904.probes.dht import DHTProbe


def main():
    cfg = _parse_args()
    common.setup(cfg)

    dht_device = adafruit_dht.DHT22(cfg.pin)
    try:
        probe = DHTProbe(dht_device)
        common.run(cfg, probe)
    finally:
        dht_device.exit()


def _parse_args():
    parser = common.new_arg_parser()
    parser.add_argument("--pin", default="D4", type=_pin, help="pin name")
    return parser.parse_args()


def _pin(value):
    try:
        return getattr(board, value)
    except AttributeError:
        raise ValueError("unknown pin value {}".format(value))


if __name__ == "__main__":
    main()
