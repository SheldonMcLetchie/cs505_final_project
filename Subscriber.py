#!/usr/bin/env python
import pyorient
import pika
import sys
import json
#import pysiddhi
from time import sleep
from connect_db import connect_db
from lib_sheldon import close_brackets



#set up data storage

client=connect_db()

#siddhiManager = SiddhiManager()

#siddhiApp = "define stream patientStream (zipcode int, patient_status_code int);" + \
#    "@info(name = 'incoming')" + \
#    "from patientStream"

# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"

username = 'student'
password = 'student01'
hostname = 'vcbumg2.cs.uky.edu'
virtualhost = '1'

credentials = pika.PlainCredentials(username, password)
parameters = pika.ConnectionParameters(hostname,
                                           5672,
                                           virtualhost,
                                           credentials)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

exchange_name = 'patient_data'
channel.exchange_declare(exchange=exchange_name, exchange_type='topic')

result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

binding_keys = "#"

if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange=exchange_name, queue=queue_name, routing_key=binding_key)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    #send data to database 
    data = json.loads(body.decode("utf-8"))
    for patient in data:
        print("*****************************************")
        print(patient)
        client.command(
            "INSERT INTO Patient CONTENT " + str(patient)
        )


channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

