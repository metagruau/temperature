# temperature

Get inside and outside temperature. Store it. Display it.

## History

### v2

V2 (current) is based on Grafana to display the data, and PostgreSQL to store
it. The sensors can send their data remotely, although it's currently based on
a "trusted sensors" approach, meaning the sensors are connecting directly to
postgres and can insert data for any source.

Ideally this would be wrapped around an HTTP API but there wasn't quite a need
for it yet.

### v1

V1 was the original approach based on Gnuplot and a simple text file format.
There was no support for remote sensors. Check the git history to view it.

## Programs

All the `read-*` programs share common options for storage and core, plus some
probe-specific options.

You have to `export PYTHONPATH=./src` to launch them from this directory.

### read-temp-dht22.py

Read temperature/humidity from a DHT22 sensor.

Dependencies:
* adafruit-circuitpython-dht (`pip install adafruit-circuitpython-dht`)
  * libgpiod2 (on Debian: `apt install libgpiod2`)

### read-temp-msc.py

Read temperature/humidity from [Meteorological Service of Canada
Datamart](https://eccc-msc.github.io/open-data/readme_en/)

### read-temp-ds18b20.py

Read temperature from a DS18B20 sensor. Requires kernel with w1\_therm driver.

### read-temp-stub.py

Generate fake temperature and humidity, useful for development to test the core
and storage and display.
