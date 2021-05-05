import pyorient
import csv
import json
import pandas as pd

#hospital zip column to dataframe
df = pd.read_csv("hospitals.csv", sep= '\t')
hospcolumn = df['ZIP']
#to list
hosplist = hospcolumn.tolist()



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
    client.command("CREATE PROPERTY Hospital.total_beds Integer")
    client.command("CREATE PROPERTY Hospital.trauma String")
    
    

    
    #create kyzipdistance class
    client.command("CREATE CLASS kyzipdistance EXTENDS V")
    client.command("CREATE PROPERTY kyzipdistance.zip_from Integer")
    client.command("CREATE PROPERTY kyzipdistance.zip_to Integer")
    client.command("CREATE PROPERTY kyzipdistance.distance Double")

    #index distance to improve query speed
    client.command("CREATE INDEX kyzipdistance.distance NOTUNIQUE")


    
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
    reset_status_code = dict()
    reset_status_code["reset_status_code"] = 0
    
    query = "DELETE VERTEX Hospital"
    client.command(query)


    white_list=["ID", "NAME", "ZIP", "BEDS", "TOTAL_BEDS", "TRAUMA"]
    with open(hospital_file,mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter = '\t')
        for row in csv_reader:
            #compress dict to just be values wanted
            short_row = { key.lower():val for (key,val) in row.items() if key in white_list}
            insert_values = json.dumps(short_row)
            client.command("INSERT INTO Hospital CONTENT " + insert_values)
    
    reset_status_code["reset_status_code"] = 1

    return json.dumps(reset_status_code)

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
    
    
    reset_status_code["reset_status_code"] = 1

    return json.dumps(reset_status_code)

def getzipalertlist():
    response = dict()
    zipalertlist=list()
    with open("zipalertlist.txt") as f:
        for line in f:
            zipalertlist.append(line.strip('\n'))
    response["ziplist"] = zipalertlist

    return json.dumps(response)

def getalertlist():
    response = dict()
    alertlist=list()
    with open("zipalertlist.txt") as f:
        for line in f:
            alertlist.append(line.strip('\n'))
    if(len(alertlist)>=5):
        response["state_status"] = "1"
    
    else:
        response["state_status"] = "0"
    

    return json.dumps(response)

def subtract_bed(zip_code,patient_status_code,hospital_zips,client):
    #staycodes = [stay home],[closest hospital ],[emercgey]
    staycodes = [[0, 1, 2, 4], [3, 5], [6]]
   
    # if patient_status_code in staycodes[0]:
    if patient_status_code in staycodes[0]:
        return 0

    elif patient_status_code in staycodes[1]:
        hospital_zip=get_min_dist_hospital_zip(zip_code,hospital_zips,client)
        if(hospital_zip != -1):
            print("hospital id: " + str(get_hospital_id(hospital_zip,client)) + " zip " + str(hospital_zip))
            sub_bed(hospital_zip,client)
            return 0
        else:
            return -1

    elif patient_status_code in staycodes[2]:
        # trama_zips 6
        trama_zips = [[40336,40456,40484,40831,41031,41472,41503,41858,42078,42437,42754],[40422,42303,42718],[41501],[40202,40536]]
        hospital_zip = get_emergency_hospital_zip(zip_code,trama_zips,client)
        if (hospital_zip != -1) :
            print("hospital id: " + str(get_hospital_id(hospital_zip,client)) + " zip " + str(hospital_zip))
            sub_bed(hospital_zip,client)
            return 0
        else:
            return -1

    

def get_min_dist_hospital_zip(zip_code,hospital_zips,client):
    str_hospitals=''.join(str(hospital_zips))
    result=client.command(
        "SELECT min(distance), zip_to AS hospital_zip FROM kyzipdistance WHERE zip_from = " + zip_code + " AND zip_to IN " + str_hospitals 
    )
    if bool(result[0].oRecordData):
        return result[0].oRecordData["hospital_zip"]
    return -1

def get_emergency_hospital_zip(zip_code,hospital_zips,client):
    str_hospitals=''.join(str(hospital_zips[0]))
    result=client.command(
        "SELECT min(distance), zip_to AS hospital_zip FROM kyzipdistance WHERE zip_from = " + zip_code + " AND zip_to IN " + str_hospitals 
    )
    if bool(result[0].oRecordData):
        return result[0].oRecordData["hospital_zip"]
    return -1

def get_hospital_id(hospital_zip,client):
    result=client.command(
        "SELECT id FROM Hospital WHERE zip = " + str(hospital_zip) + " LIMIT 1"
    )

    return result[0].oRecordData["id"]


def sub_bed(hospital_zip,client):
    client.command(
        "UPDATE Hospital INCREMENT beds = -1 WHERE zip = " + str(hospital_zip)
    )
    #maybe build edge here? help with OF 2
    # WHERE hospital_zip = " + str(hospital_zip)

def getbeds(id,client):
    result=client.command(
        "SELECT total_beds, beds , zip FROM Hospital WHERE id = " + id
    )

    return result[0].oRecordData

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
   
    #reporting to closest facility
    if patientstat in (3,5):

        #get zipcode
        FCF = client.query("SELECT zip_code FROM patient where mrn = " +  "'"+ mrn + "'")
        k = FCF[0].oRecordData
        zipcd = k['zip_code']

       #get zipcode in hospital.csv with the smallest distance 
        CFF = client.query("SELECT * FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'" + " AND "+ "zip_to in " + str(hosplist) + " ORDER BY distance LIMIT 1")
        z = CFF[0].oRecordData
        mindist = z['zip_to']
        

        #find hospital id of the zipcode that has the minimum distance
        CKK = client.query("SELECT id FROM hospital where zip = " + str(mindist))
        h = CKK[0].oRecordData
        closesthospitalid = h['id']

        return (closesthospitalid)

    elif patientstat in (0,1,2,4):
        return (0)

    elif patientstat == 6:
        #get zipcode
        FCF = client.query("SELECT zip_code FROM patient where mrn = " +  "'"+ mrn + "'")
        k = FCF[0].oRecordData
        zipcd = k['zip_code']
        
        #-----
        traumalist = [41858, 42437, 42754, 41031, 40456, 41472, 40336, 40831, 40484, 41503, 42078]
        
       #get zipcode in hospital.csv with the smallest distance and trauma = LEVEL IV
        
        CFF = client.query("SELECT * FROM kyzipdistance WHERE zip_from = " +  "'"+ zipcd + "'" + " AND "+ "zip_to in " + str(traumalist) + " ORDER BY distance LIMIT 1")
        z = CFF[0].oRecordData
        mindist = z['zip_to']
       
       #find hospital id of the zipcode that has the minimum distance
        CFG = client.query("SELECT id FROM hospital WHERE zip = " + str(mindist))
        d = CFG[0].oRecordData
        closesthospid = d['id']
        
        return(closesthospid)
    else:
        return(-1)

