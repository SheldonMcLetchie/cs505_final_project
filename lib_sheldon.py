import pyorient
import csv
import json

def create_db():
    #database name
    dbname = "disk"
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
        dbname,
        pyorient.DB_TYPE_GRAPH,
        pyorient.STORAGE_TYPE_PLOCAL
        #pyorient.STORAGE_TYPE_MEMORY # for memory storage.
    )

    #create patient class
    client.command("CREATE CLASS Patient extends V")
    client.command("CREATE PROPERTY Patient.first_name String")
    client.command("CREATE PROPERTY Patient.last_name String")
    client.command("CREATE PROPERTY Patient.mrn String")
    client.command("CREATE PROPERTY Patient.zipcode Integer")
    client.command("CREATE PROPERTY Patient.patient_status_code Integer")

    #create hospital class
    client.command("CREATE CLASS Hospital extends V")
    client.command("CREATE PROPERTY Hospital.id Integer")
    client.command("CREATE PROPERTY Hospital.name String")
    client.command("CREATE PROPERTY Hospital.zip Integer")
    client.command("CREATE PROPERTY Hospital.beds Integer")
    client.command("CREATE PROPERTY Hospital.trauma String")
    
    #create kyzipdistance class
    client.command("CREATE CLASS kyzipdistance EXTENDS V")
    client.command("CREATE PROPERTY kyzipdistance.zip_from Integer")
    client.command("CREATE PROPERTY kyzipdistance.zip_to Integer")
    client.command("CREATE PROPERTY kyzipdistance.distance Double")
    
    client.close()

def close_brackets(str):
    return str+"}"

def dump_db(client,className):
    query = "SELECT FROM " + className
    data = client.query(query)
    return ''.join(str(x) for x in data)

def dump_row_count(client,className):
    query = "SELECT COUNT(*) as count FROM " + className
    data = client.query(query)
    return ''.join(str(x) for x in data)

def load_hospital(client,hospital_file):
    white_list=["ID", "NAME", "ZIP", "BEDS", "TRAUMA"]
    with open(hospital_file,mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = '\t')
        for row in csv_reader:
            #compress dict to just be values wanted
            short_row = { key.lower():val for (key,val) in row.items() if key in white_list}
            insert_values = json.dumps(short_row)
            client.command("INSERT INTO Hospital CONTENT " + insert_values)

def load_kydist(client,kydist_file):
     with open(kydist_file,mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = ',')
        for row in csv_reader:
            #compress dict to just be values wanted
            insert_values = json.dumps(row)
            print(insert_values)
            client.command("INSERT INTO kyzipdistance CONTENT " + insert_values)

def reset_patient(client):
    reset_status_code = dict()
    reset_status_code["reset_status_code"] = 0
    
    query = "DELETE VERTEX Patient"
    client.command(query)
    
    #try:
    #    client.command(query)
    #except pyorient.exceptions:
    #    return json.dumps(reset_status_code)
    
    reset_status_code["reset_status_code"] = 1

    return json.dumps(reset_status_code)