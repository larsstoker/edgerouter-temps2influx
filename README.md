# Edgerouter Temperatures to InfluxDB
This container will query your Edgerouter every 30 seconds for the CPU, PNY and Board temperatures and export it to InfluxDB.

## Usage
```shell
docker run larsstoker/edgerouter-temps2influx:latest
```

#### Environment Variables

* `EDGEROUTER_HOST` - Edgerouter hostname
* `EDGEROUTER_USR` - Edgerouter username
* `EDGEROUTER_PWD` - Edgerouter password
* `INFLUX_HOST` - InfluxDB hostname
* `INFLUX_USR` - InfluxDB user
* `INFLUX_PWD` - InfluxDB password
* `INFLUX_DB` - InfluxDB database


![example-grafana](https://i.imgur.com/I6T2CNG.png)
