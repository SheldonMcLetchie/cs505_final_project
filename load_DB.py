from lib_sheldon import create_db, load_hospital, load_kydist

create_db()
 client=connect_db()
# load data
hospital_file="hospitals.csv"
load_hospital(client,hospital_file)

#takes 12 mins to load. Need script to make kyzipdistance smaller
kydist_file = "kyzipdistance.csv"
load_kydist(client,kydist_file)