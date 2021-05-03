#!/bin/bash
# This script is for running the project clean. It includes compliing java
# run as:
# nohup run_full.sh &
cd cs505-pubsub-cep-template-master/
sudo mvn clean package
cd ..

sudo docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb:2.2
Python3 load_DB.py

Python3 Subscriber.py &
sudo java -jar cs505-pubsub-cep-template-master/target/cs505-pubsub-cep-template-1.0-SNAPSHOT.jar &

Python3 main.py