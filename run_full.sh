#!/bin/bash
# This script is for running the project clean. It includes compliing java
# to run in background:
# nohup run_full.sh &
# to run indivually run each line, removing '>> /dev/null 2>&1 &''
cd cs505-pubsub-cep-template-master/
sudo mvn clean package
cd ..

#skip this if the container already has data from load_DB.py
sudo docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb:2.2
python3 load_DB.py

#run to start subscribers for orient and siddhi
python3 Subscriber.py >> /dev/null 2>&1 &
sudo java -jar cs505-pubsub-cep-template-master/target/cs505-pubsub-cep-template-1.0-SNAPSHOT.jar >> /dev/null 2>&1 &

#start webserver
python3 main.py