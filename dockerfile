FROM Nginx:latest

RUN apt-get update && apt-get install -y git\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/share/nginx/html
