# cs505_final_project
This is the repo for the cs505 project

1. Set-up reference "Working with Graph Databases" and "My CEP" for the two databases and "exposing services in a custom container" for the webconnection.

2. Docker images required:
    orientdb:2.2
    rabbitmq:latest
    Nginx - webserver

3. To launch docker on webserver 

docker run -it --rm -d -p 8080:80 --name web -v ~/site-content:/usr/share/nginx/html nginx