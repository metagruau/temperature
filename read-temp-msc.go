package main

import (
	"encoding/xml"
	"fmt"
	"io"
	"net/http"
	"strconv"
	"time"
)

// XXX maybe should be rewritten in python lol, so we have only one language for probes and can reuse
//     code some more

type Observation struct {
	Time        time.Time
	Temperature float64 // in Celsius
	Humidity    int     // relative humidity precentage, between 0 and 100
}

func main() {
	// TODO add options similar to read-temp-dht22

	probe := NewMSCDatamartProbe("https://dd.weather.gc.ca/observations/swob-ml/latest/CWQB-AUTO-minute-swob.xml")
	for {
		obs, err := probe.Observe()
		if err != nil {
			// TODO improve logging (stderr) and error handling
			fmt.Printf("Failed to observe: %v\n", err)
		} else {
			output(obs, false)
		}

		time.Sleep(600 * time.Second)
	}
}

// MSC stands for Meteorological Service of Canada
type MSCDatamartProbe struct {
	client *http.Client
	url    string
}

func NewMSCDatamartProbe(url string) *MSCDatamartProbe {
	return &MSCDatamartProbe{
		client: &http.Client{
			Timeout: 10 * time.Second,
		},
		url: url,
	}
}

func (p *MSCDatamartProbe) Observe() (*Observation, error) {
	resp, err := p.client.Get(p.url)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	defer io.Copy(io.Discard, resp.Body)

	if resp.StatusCode != 200 {
		return nil, fmt.Errorf("Unexpected status code %v received", resp.StatusCode)
	}

	return getObservationFromSwobXml(resp.Body)
}

func getObservationFromSwobXml(r io.Reader) (*Observation, error) {
	// this is a rather fragile implementation, there's a few way this could break
	// if new fields are added in the XML document
	// TODO add some tests
	// XXX function does not guarantee that XML body is fully read from io.Reader, might
	//     cause some issues depending on how the reader is used above
	// TODO we could use decoder.DecodeElement to tidy things up a little
	decoder := xml.NewDecoder(r)
	inSamplingTime := false
	inTimePosition := false
	obs := Observation{}
	timeIsSet := false
	temperatureIsSet := false
	humidityIsSet := false

	for {
		token, err := decoder.RawToken()
		if token == nil && err == io.EOF {
			break
		} else if err != nil {
			// TODO log to stderr
			fmt.Printf("Error while parsing SWOB-XML: %v\n", err)
			return nil, err
		}

		switch t := token.(type) {
		case xml.StartElement:
			switch t.Name.Local {
			case "element":
				// extract name and value attributes
				var name, value string
				for _, attr := range t.Attr {
					switch attr.Name.Local {
					case "name":
						name = attr.Value
					case "value":
						value = attr.Value
					}
				}

				switch name {
				case "air_temp":
					if !temperatureIsSet {
						if v, err := strconv.ParseFloat(value, 64); err != nil {
							// TODO log to stderr
							fmt.Printf("Failed to parse temperature value: %v\n", err)
						} else {
							obs.Temperature = v
							temperatureIsSet = true
						}
					}
				case "rel_hum":
					if !humidityIsSet {
						if v, err := strconv.ParseInt(value, 10, 32); err != nil {
							// TODO log to stderr
							fmt.Printf("Failed to parse humidity value: %v\n", err)
						} else {
							obs.Humidity = int(v)
							humidityIsSet = true
						}
					}
				}
			case "timePosition":
				inTimePosition = true
			case "samplingTime":
				inSamplingTime = true
			}
		case xml.CharData:
			if inTimePosition && inSamplingTime {
				if v, err := time.Parse("2006-01-02T15:04:05.000Z", string(t)); err != nil {
					// TODO log to stderr
					fmt.Printf("Failed to parse time value: %v\n", err)
				} else {
					obs.Time = v
					timeIsSet = true
				}
			}
		case xml.EndElement:
			switch t.Name.Local {
			case "timePosition":
				inTimePosition = false
			case "samplingTime":
				inSamplingTime = false
			}
		}
	}

	if !timeIsSet || !temperatureIsSet || !humidityIsSet {
		// TODO log to stderr
		fmt.Printf("Not all values were set (time %v, temperature %v, humidity %v)\n", timeIsSet, temperatureIsSet, humidityIsSet)
		// XXX lame error
		return nil, fmt.Errorf("value not set")
	}

	return &obs, nil
}

func output(obs *Observation, utc bool) {
	var t time.Time
	if utc {
		t = obs.Time.UTC()
	} else {
		t = obs.Time.Local()
	}

	fmt_dt := t.Format("20060102T150405")
	fmt.Printf("%s\t%.1f\t%d\n", fmt_dt, obs.Temperature, obs.Humidity)
}
