#!/usr/bin/env python
from influxdb import InfluxDBClient
import subprocess
import socket

hostname = socket.gethostname()
client = InfluxDBClient(host='hostname', port=8086, username='admin', password='password')

cpuTemp = subprocess.check_output('/usr/sbin/ubnt-hal' + ' getTemp'  """ | grep CPU: | cut -c 5- | sed 's/..$//' """"", shell=True)
boardTemp = subprocess.check_output('/usr/sbin/ubnt-hal' + ' getTemp'  """ | grep Board | sed -n '1p' | cut -c 13- | sed 's/..$//' """"", shell=True)

createdb = client.create_database('edgerouter')

def RUN():
        createdb
        measurement = {}
        measurement['measurement'] = 'edgerouter'
        measurement['tags'] = {}
        measurement['tags'] ['hostname'] = str(hostname)
        measurement['fields'] = {}
        measurement['fields']['cpuTemp'] = str(cpuTemp.strip())
        measurement['fields']['boardTemp'] = str(boardTemp.strip())
        client.switch_database('edgerouter')
        client.write_points([measurement])
        print((cpuTemp.strip()) + str("C"))
        print("Data written to DB")
RUN()
# EOF