from influxdb import InfluxDBClient
import pexpect
import json
from pathlib import Path
from os import environ

#Load enviornment variables
#Edgerouter vars
er_host = environ['ER_HOST']
er_usr = environ['ER_USR']
er_pwd = environ['ER_PWD']
#DB vars
# db_host = environ['DB_HOST']
# db_database = environ['DB_DATABASE']
# db_usr = environ['DB_USR']
# db_pwd = environ['DB_PWD']

class Edgerouter:
    def __init__(
                self,
                host,
                usr,
                pwd
        ):
        self.host = host
        self.usr = usr
        self.pwd = pwd
        
        self.session = self.connect()

    #Connect to Edgerouter
    def connect(self):
        child = pexpect.spawn('ssh ' + self.usr + '@' + self.host, maxread=16384)
        code = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:'])
        if code == 0:
            child.sendline('yes')
            code = child.expect(['Are you sure you want to continue connecting (yes/no)?', 'password:'])
        if code == 1:
            child.sendline(self.pwd)
        child.expect('$')
        return child

    #Get CPU Temp
    def GetCpuTemp(self):
        self.session.sendline('show hardware temperature')
        self.session.expect_exact('CPU:')

        return(self.session.read(2).decode('utf-8'))
    
    #Get PHY Temp
    def GetPhyTemp(self):
        self.session.sendline('show hardware temperature')
        self.session.expect_exact('PHY:')

        return(self.session.read(2).decode('utf-8'))

    #Get Board Temp
    def GetBoardTemp(self):
        self.session.sendline('show hardware temperature')
        self.session.expect_exact('Board (CPU):')

        return(self.session.read(2)).decode('utf-8')

    #Get Edgerouter Hostname
    def GetHostname(self):
        self.session.sendline('show host name')
        self.session.expect("")

        return(self.session.read())

# #Export data to influx
# def exportInflux(host, db, usr, pwd):
#     client = InfluxDBClient(host=host, db=db , username=usr, password=pwd, port=8086)

#     client.create_database(db)
#     measurement = {}
#     measurement['measurement'] = 'edgerouter'
#     measurement['tags'] = {}
#     measurement['tags']['hostname'] = str(hostname())
#     measurement['fields'] = {}
#     measurement['fields']['value'] = str(cpuTemp().decode('utf-8'))
#     client.switch_database(db)
#     client.write_points([measurement])

def main():
#   try:
    er = Edgerouter(er_host, er_usr, er_pwd)
    print(er.GetHostname())
#   finally:
#     exportInflux(db_host, db_database, db_usr, db_pwd)

if __name__ == "__main__":
  main()
#EOF