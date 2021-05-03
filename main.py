import json
from flask import Flask
import socket
import time
from lib_sheldon import dump_db, dump_row_count, reset_patient, getlocationcode, getzipalertlist
from connect_db import connect_db


def launch_web_api():
    # launch Database   
    client=connect_db()

    # launch web application
    app = Flask(__name__)  

    # testing APIs
    @app.route('/test/')
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



    #MF1 API
    @app.route('/api/getteam')
    def getteam():

        team = dict()
        team['team_name'] = "505Team"
        team['Team_members_sids'] = ["12535791", "10456246"]
        team['app_status_code'] = "1"

        #encode and respond
        return json.dumps(team)


    @app.route('/api/getpatient/<string:mrn>/')
    def getpatient(mrn):

        location_code = getlocationcode(mrn)

        patient = dict()
        patient['mrn'] = str(mrn)
        patient['location_code'] = str(location_code)
        

        #encode and respond
        return json.dumps(patient)


    #-----------------------------------------#

    #RTR1
    @app.route('/api/zipalertlist')
    def zipalertlist():
        return getzipalertlist()

    #reset
    @app.route('/api/reset')
    def reset():
        return reset_patient(client)

    return app



if __name__ == '__main__':
    #listen on all interfaces on port 9000
    launch_web_api().run(host='0.0.0.0', port=9000)


