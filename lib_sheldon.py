import pyorient

def create_db():
    #database name
    dbname = "local"
    #database login is root by default
    login = "root"
    #database password, set by docker param
    password = "rootpwd"

    #create client to connect to local orientdb docker container
    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect(login, password)
    
    #dropping old database
    if client.db_exists(dbname):
        client.db_drop(dbname)

    #Create new orientdb database
    client.db_create(
        pyorient.DB_TYPE_GRAPH,
        pyorient.STORAGE_TYPE_PLOCAL
        #pyorient.STORAGE_TYPE_MEMORY # for memory storage.
    )

    #create nodes and edges
    

def load_db(filepath):
  

    #open the database we are interested in
    client.db_open(dbname, login, password)
    #create schema
    #load in the data?

    client.close()
