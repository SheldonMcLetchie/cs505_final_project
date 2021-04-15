import json
from flask import Flask
import socket
import time

def launch_web_api():
    app = Flask(__name__)

    @app.route('/')
    def get_status():
        #query
        start_time = time.time()
        hostname = socket.gethostname()
        current_time = time.time()
        exec_time = time.time() - start_time
        status = 'online'

        #package
        responce = dict()
        responce['hostname'] = hostname
        responce['current_time'] = current_time
        responce['exec_time'] = exec_time
        responce['status'] = status

        #encode and respond
        return json.dumps(responce)


    return app

if __name__ == '__main__':
    #listen on all interfaces on port 9000
    launch_web_api().run(host='0.0.0.0', port=9000)

