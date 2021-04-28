import json
from flask import Flask
import socket
import time
from lib_sheldon import dump_db, dump_row_count
from connect_db import connect_db


def launch_web_api():
    # launch Database   
    client=connect_db()

    # launch web application
    app = Flask(__name__)  

    # testing APIs
    @app.route('/test')
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
    
    @app.route('/patient_dumpdata')
    def patient_dump():
        return dump_db(client,"Patient")
    
    @app.route('/hospital_dumpdata')
    def hospital_dump():
        return dump_db(client,"Hospital")

    @app.route('/kydist_count')
    def kydist_dump():
        return dump_row_count(client,"kyzipdistance")
    # project APIs
    return app


if __name__ == '__main__':
    #listen on all interfaces on port 9000
    launch_web_api().run(host='0.0.0.0', port=9000)


