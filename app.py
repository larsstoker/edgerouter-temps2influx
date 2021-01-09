#!/usr/bin/env python3
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
import pexpect
import logging
import time
import schedule
from pathlib import Path
from os import environ

edgerouter_host = environ['EDGEROUTER_HOST']
edgerouter_usr = environ['EDGEROUTER_USR']
edgerouter_pwd = environ['EDGEROUTER_PWD']
influx_host = environ['INFLUX_HOST']
influx_usr = environ['INFLUX_USR']
influx_pwd = environ['INFLUX_PWD']
influx_db = environ['INFLUX_DB']

class Edgerouter:
  connection = ""
  # Login to edgerouter
  def login(host, username, password):
      global connection
      connection = pexpect.spawn("ssh " + username + "@" + host, maxread=16384)
      code = connection.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:'])
      if code == 0:
        connection.sendline('yes')
        code = connection.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:'])
      if code == 1:
        connection.sendline(password)
      connection.expect("$")
  # endDef
  
  # Get CPU Temp
  def cpuTemp():
      connection.sendline("show hardware temperature")
      connection.expect("CPU:")
      temp = connection.read(2).decode("utf-8")

      print("CPU Temperature is: " + temp + "°C")
      return temp
  # endDef

    # Get PHY Temp
  def phyTemp():
      connection.sendline("show hardware temperature")
      connection.expect("PHY:")
      temp = connection.read(2).decode("utf-8")

      print("PHY Temperature is: " + temp + "°C")
      return temp
  # endDef

  # Get Board Temp
  def boardTemp():
      connection.sendline("show hardware temperature")
      connection.expect_exact("Board (CPU):")
      temp = connection.read(2).decode("utf-8")

      print("Board Temperature is: " + temp + "°C")
      return temp
  # endDef

# Export to InfluxDB
def export_influxdb(host,user,password,db):
  #Influx client 
  client = InfluxDBClient(
    host=influx_host,
    port=8086,
    username=influx_usr,
    password=influx_pwd
  )

  measurement = {}
  measurement['measurement'] = 'edgerouter'
  measurement['tags'] = {}
  measurement['tags']['hostname'] = str(edgerouter_host)
  measurement['fields'] = {}
  measurement['fields']['cpuTemp'] = str(Edgerouter.cpuTemp())
  measurement['fields']['phyTemp'] = str(Edgerouter.phyTemp())
  measurement['fields']['BoardTemp'] = str(Edgerouter.boardTemp())
  try:
    client.switch_database(db)
    client.write_points([measurement])
    print("Exported to InfluxDB successfully")
    print("")
  except InfluxDBClientError as e:
    logging.error("Failed to export data to Influxdb: %s" % e)
#endDef

def main():
  Edgerouter.login(edgerouter_host, edgerouter_usr, edgerouter_pwd)
  export_influxdb(influx_host, influx_usr, influx_pwd, influx_db)
#endDef

if __name__ == "__main__":
  print("Starting Edgerouter Temp2Influx...")
  main()
  schedule.every(1).minutes.do(main)
  while 1:
    schedule.run_pending()
    time.sleep(1)