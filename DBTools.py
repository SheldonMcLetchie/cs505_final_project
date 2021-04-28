import pyorient
import json
import re


def reset_db(client, name):

   # Remove Old Database
   if client.db_exists(name):
    client.db_drop(name)

   # Create New Database
   client.db_create(name,
      pyorient.DB_TYPE_GRAPH,
      pyorient.STORAGE_TYPE_PLOCAL)

def getrid(client,id):
    nodeId = client.query("SELECT FROM V WHERE id = '" + str(id) + "'")
    return str(nodeId[0]._rid)





def loadDB(filepath):

    #database name
    dbname = "disk"
    #database login is root by default
    login = "root"
    #database password, set by docker param
    password = "rootpwd"

    #create client to connect to local orientdb docker container
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect(login, password)

    #remove old database and create new one
    reset_db(client,dbname)

    #open the database we are interested in
    client.db_open(dbname, login, password)

    client.command("CREATE CLASS Hospitals EXTENDS V")

    client.command("CREATE PROPERTY Hospitals.zip_from String")
    #name
    client.command("CREATE PROPERTY Hospitals.zip_to String")
    #id
    client.command("CREATE PROPERTY Hospitals.distance Integer")

    #open and parse local json file
    with open(filepath) as f:
        data = json.load(f)

    #loop through each key in the json database and create a new vertex, V with the id in the database
    for key in data:
        #name = data.get(key).get("name")
        zip_to = re.sub("'", "", data.get(key).get("zip_to"))

        distance = re.sub("'", "", data.get(key).get("distance"))

        zip_from = re.sub("'", "", data.get(key).get("zip_from"))

        

        #print("CREATE VERTEX Person SET id = '" + key + "', name = '" + name + "'")
        client.command("CREATE VERTEX Hospital SET zip_from = '" + zip_from + "', zip_to = '" + zip_to + "', distance = '" + distance + "'")

        


        

    #loop through each key creating edges from advisor to advisee

    client.close()


