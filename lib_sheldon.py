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

#----------------------


def getlocationcode(mrn):


    dbname = "disk"
    login = "root"
    password = "rootpwd"

    client = pyorient.OrientDB("localhost", 2424)
    session_id = client.connect(login, password)

    client.db_open(dbname, login, password)

    #check status code
    PSC = client.query("SELECT patient_status_code FROM patient where mrn = " +  "'"+ mrn + "'")

    p = PSC[0].oRecordData

    patientstat = p['patient_status_code']
    #print("PatientStatus", patientstat)
   
    #reporting to closest facility
    if patientstat in (3,5):
        #get zipcode
        FCF = client.query("SELECT zip_code FROM patient where mrn = " +  "'"+ mrn + "'")
        k = FCF[0].oRecordData
        zipcd = k['zip_code']

       
       #get closest zipcode to patient zip
        CFF = client.query("SELECT MIN(distance) FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'")
        z = CFF[0].oRecordData
        mindist = z['MIN']

        CFG = client.query("SELECT zip_to FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'" + "AND " + "distance = " +str(mindist))
        y = CFG[0].oRecordData
        closestzip = y['zip_to']

        #hospitalID of zipcode
        CZH = client.query("SELECT id FROM hospital where zip = " + str(closestzip))
        b = CZH[0].oRecordData
        closesthospitalid = b['id']
        
        #print(closesthospitalid)

        return (closesthospitalid)
    elif patientstat in (0,1,2,4):
        return (0)
    elif patientstat == 6:
        FCF = client.query("SELECT zip_code FROM patient where mrn = " +  "'"+ mrn + "'")
        k = FCF[0].oRecordData
        zipcd = k['zip_code']
        
        #print("patient zip", zipcd)
       
       #get closest zipcode to patient zip
        CFF = client.query("SELECT MIN(distance) FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'")
        z = CFF[0].oRecordData
        mindist = z['MIN']

        CFG = client.query("SELECT zip_to FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'" + "AND " + "distance = " +str(mindist))
        y = CFG[0].oRecordData
        closestzip = y['zip_to']

        #hospitalID of zipcode
        CZH = client.query("SELECT id FROM hospital where zip = " + str(closestzip) + " AND " + "trauma = 'LEVEL IV'")
        b = CZH[0].oRecordData
        closesthospitalid = b['id']
        
        return (closesthospitalid)
    else:
        return(-1)
    

