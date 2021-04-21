def connect_db():
    #create client to connect to local orientdb docker container
    client = pyorient.OrientDB("localhost", 2424)

    #database name
    dbname = "local"
    #database login is root by default
    login = "root"
    #database password, set by docker param
    password = "rootpwd"

    client.db_open(dbname,login,password)

    return client