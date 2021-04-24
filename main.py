

import json
from flask import Flask
import socket
import time
from lib_sheldon import create_db, dump_db
from connect_db import connect_db


def launch_web_api():
    # launch Database
    create_db()
    client=connect_db()
    # launch web application
    app = Flask(__name__)

    @app.route('/trial')
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

    #resets the database
    @app.route('/reset')
    def db_reset():
        message ="I was not reset"
        return json.dumps(message)
    
    @app.route('/local_dumpdata')
    def dumpdata():
        return dump_db(client)
        
  
    return app


if __name__ == '__main__':
    #listen on all interfaces on port 9000
    launch_web_api().run(host='0.0.0.0', port=9000)


