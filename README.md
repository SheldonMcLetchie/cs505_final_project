# cs505_final_project
This is the repo for the cs505 project


#Running project
1. Start orientdb container

docker run -d --name orientdb -p 2424:2424 -p 2480:2480 -e ORIENTDB_ROOT_PASSWORD=rootpwd orientdb:2.2

2. start main.py (starts the web api)
Python3 main.py

3. start Subscriber.py
Python3 Subscriber.py


#Set up
I. Git
1. sudo git clone https://github.com/SheldonMcLetchie/cs505_final_project.git

2. On the VM to work on a specific branch do:
    git checkout <branch-name>

3. make sure code works on branch before pushing to main. 

II. Install rabbitmq (not 100% sure this is required)
Detailed directions:
https://www.rabbitmq.com/install-debian.html#erlang-repositories

Quick directions:

1. ```sudo apt-get update -y```

2. ```sudo apt-get install curl gnupg debian-keyring debian-archive-keyring -y```

3. ```curl -fsSL https://github.com/rabbitmq/signing-keys/releases/download/2.0/rabbitmq-release-signing-key.asc | sudo apt-key add -```

4. ```sudo apt-key adv --keyserver "keyserver.ubuntu.com" --recv-keys "F77F1EDA57EBB1CC"```

5. ```sudo apt-get install apt-transport-https```

Note: I didn't do 6 or 7 and still got output

6. ```deb http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu focal main```

7. ```deb-src http://ppa.launchpad.net/rabbitmq/rabbitmq-erlang/ubuntu focal main```

end of note 

8. ```sudo apt-get update -y```

9.

```
  sudo apt-get install -y erlang-base \
                        erlang-asn1 erlang-crypto erlang-eldap erlang-ftp erlang-inets \
                        erlang-mnesia erlang-os-mon erlang-parsetools erlang-public-key \
                        erlang-runtime-tools erlang-snmp erlang-ssl \
                        erlang-syntax-tools erlang-tftp erlang-tools erlang-xmerl


III. Install pika (for rabbitmq) 


sudo pip3 install pika

IV. Install pysiddhi (https://siddhi.io/en/v5.1/docs/examples/)

sudo pip3 install pysiddhi



