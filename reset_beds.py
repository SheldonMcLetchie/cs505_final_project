from lib_sheldon import load_hospital
from connect_db import connect_db

client=connect_db()
hospital_file="hospitals_totalbed.txt"

load_hospital(client,hospital_file)