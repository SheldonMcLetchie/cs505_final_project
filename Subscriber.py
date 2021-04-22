#!/usr/bin/env python
import pika
import sys
import json
import pyorient
from connect_db import connect_db
from lib_sheldon import close_brackets

#connect to the orientdb
client=connect_db()
dbname = "local"

# Set the connection parameters to connect to rabbit-server1 on port 5672
# on the / virtual host using the username "guest" and password "guest"

username = 'student'
password = 'student01'
hostname = '128.163.202.50'
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
    print("----------------------------------------------")
    print()
    print(" [x] %r:%r" % (method.routing_key, body))
    print("-----------------------------------------------")
    print()

    #send data to database
    json_str = str(body)[1:]
    json_str = json_str.replace('\'','').replace('[','').replace(']','')

    patients = json_str.split("},")
    patients = [x.close_brackets() for x in patients]
    print(patients)
    client.command(
        "INSERT INTO Patient CONTENT " + json_str
    )




channel.basic_consume(
    queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()

