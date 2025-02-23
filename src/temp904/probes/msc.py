from temp904 import Observation
from .core import ProbeCapabilities

import datetime
import logging
import urllib.request
from xml.etree import ElementTree

logger = logging.getLogger(__name__)


class MSCDatamartProbe:
    _DEFAULT_TIMEOUT = 15
    _XML_NS_MAP = {
        "default": "http://dms.ec.gc.ca/schema/point-observation/2.0",
        "gml": "http://www.opengis.net/gml",
        "om": "http://www.opengis.net/om/1.0",
    }

    capabilities = ProbeCapabilities(
        has_temperature=True,
        has_humidity=True,
        min_interval=60.0,
    )

    def __init__(self, url):
        self._url = url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def observe(self):
        with urllib.request.urlopen(self._url, timeout=self._DEFAULT_TIMEOUT) as fobj:
            obs = self._get_observation_from_swob_xml(fobj)
        return obs

    def _get_observation_from_swob_xml(self, fobj):
        tree = ElementTree.parse(fobj)
        result = tree.find("./om:member/om:Observation/om:result/default:elements", self._XML_NS_MAP)
        air_temp = result.find("./default:element[@name='air_temp']", self._XML_NS_MAP)
        rel_hum = result.find("./default:element[@name='rel_hum']", self._XML_NS_MAP)
        sampling_time = tree.find("./om:member/om:Observation/om:samplingTime/gml:TimeInstant/gml:timePosition", self._XML_NS_MAP)

        temperature = float(air_temp.attrib["value"])
        humidity = int(rel_hum.attrib["value"])
        dt = datetime.datetime.strptime(sampling_time.text, "%Y-%m-%dT%H:%M:%S.000Z")
        ts = dt.replace(tzinfo=datetime.timezone.utc).timestamp()
        return Observation(ts, temperature, humidity)

    @classmethod
    def new_station_quebec(cls):
        return cls("https://dd.weather.gc.ca/observations/swob-ml/latest/CWQB-AUTO-minute-swob.xml")
        #return cls("https://dd.weather.gc.ca/observations/swob-ml/latest/CYQB-MAN-swob.xml")
