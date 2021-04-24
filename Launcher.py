import json
import random

import socket


#from DBTools import printJSONDB
from DBTools import loadDB
#from DBTools import shortestPath

#Make sure orientDB version 2.2 is running, version 3.x does not work with these drivers

#-d run in background login:root password:rootpwd
#docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb:2.2

#-it run in foreground login:root password:rootpwd
#docker run -it --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb:2.2

#path to json file
filepath = 'kydistance.json'

#example of how to parse elements from JSON file
#printJSONDB(filepath)

#loadDB with JSON data, removing existing database if it exist
#comment the load command after the database is loaded



# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# s.settimeout(100000)

# try:
loadDB(filepath)


# except socket.timeout:
#     print("Timeout raised and caught.")


