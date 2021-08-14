# temperature

Get inside and outside temperature. Store it. Make the current temperature and
some historical data available through a very simple web page.

This is a work in progress... and the name is... duh.

## read-temp-dht22.py

Python program to read temperature/humidity from a DHT22 sensor.

Dependencies:
* adafruit-circuitpython-dht (`pip install adafruit-circuitpython-dht`)
  * libgpiod2 (on Debian: `apt-get install libgpiod2`)

Example:
```
read-temp-dht22.py --interval 600 --pin D4
```

## read-temp-msc

Go program to read temperature/humidity from [Meteorological Service of Canada
Datamart](https://eccc-msc.github.io/open-data/readme_en/)

To cross-compile for a Raspberry Pi 1:
```
GOARCH=arm GOARM=6 GOOS=linux go build read-temp-msc.go
```

Example:
```
read-temp-msc
```

## extract-data.py

Python program to filter observations.

Example to output only observations for the day of 2021-08-02:
```
extract-data.py --date-min 20210802T0000 --date-max 20210803T0000 < observations.txt
```

## plot-simple-\*.sh

Shell scripts to generate SVG images from observations.

Dependencies:
* gnuplot (on Debian: `apt-get install gnuplot-nox`)

Example to graph the last day of observations:
```
plot-simple-temperature.sh inside.txt outside.txt > temperature.svg
```
