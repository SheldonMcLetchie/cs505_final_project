from lib_sheldon import create_db, load_hospital, load_kydist
from connect_db import connect_db

create_db()
client=connect_db()
# load data
hospital_file="hospitals_totalbed.txt"
load_hospital(client,hospital_file)

#takes 12 mins to load. Need script to make kyzipdistance smaller
kydist_file = "kyzipdistance.csv"
load_kydist(client,kydist_file)