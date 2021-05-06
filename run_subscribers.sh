#!/bin/bash
python3 Subscriber.py >> /dev/null 2>&1 &
sudo java -jar cs505-pubsub-cep-template-master/target/cs505-pubsub-cep-template-1.0-SNAPSHOT.jar >> /dev/null 2>&1 &