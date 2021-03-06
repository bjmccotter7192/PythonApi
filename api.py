import flask
import json
import db
from pprint import pprint
from flask import jsonify, request
from flask_cors import CORS
import plotly.graph_objects as go
import plotly.io as pio

def create_app(test_config=None):
    app = flask.Flask(__name__)
    CORS(app)

    @app.route('/test', methods=['GET'])
    def testGet():
        return {
            "id": 1,
            "name": "Beej",
            "number": 123456789,
            "street_addr": "123 Something Street",
            "city": "SomeCity",
            "state": "State City",
            "zip": 11111 
        }, 200

    @app.route('/getClients', methods=['GET'])
    def getClients():
        conn = db.connectToDb()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients;")
        query_results = cur.fetchall()

        rows = []
        for i in query_results:
            rows.append({
                "client_id": i[0],
                "first_name": i[1],
                "last_name": i[2],
                "mi_initial": i[3],
                "number1": i[4],
                "number2": i[5],
                "email_address": i[6],
                "realtor": i[7],
                "referred_by": i[8]
            })

        print(rows)
        cur.close() 
        conn.close()

        return jsonify(rows)

    @app.route('/getGraph', methods=['GET'])
    def getGraph():
        print("INSIDE GET GRAPH")
        returnData = []
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

        for num, month in enumerate(months, start=1):
            returnData.append({
                "name": month,
                "value": num
            })

        return jsonify(returnData)

    @app.route('/addClient', methods=['GET'])
    def addClient():

        try:
            conn = db.connectToDb()
            cur = conn.cursor()
            cur.execute("INSERT INTO clients (first_name, lastname, mi_initial) VALUES (%s, %s, %s)", ("yabba", "dadda", "do",))

            conn.commit()
            cur.close() 
            conn.close()

            print("INSIDE FAILED ADD CLIENT")

            return jsonify(returnData)
        except Exception as ex:
            print("Failed to insert client into db")

    @app.route('/uploadFile', methods=['POST'])
    def uploadFile():
        requestData = json.loads(request.data)

        # try:
        conn = db.connectToDb()
        cur = conn.cursor()
        cur.execute("INSERT INTO file_uploads (file_name, file_path, file_data) VALUES (%s, %s, %s)", 
        (requestData.get('name'), requestData.get('file'), requestData.get('fileSource'),))

        conn.commit()
        cur.close() 
        conn.close()

        return {
            "Success": "WE DID IT"
        }

    @app.route('/getFiles', methods=['GET'])
    def getFiles():
        # try:
        print("Inside the getFiles Endpoint")
        conn = db.connectToDb()
        cur = conn.cursor()
        cur.execute("SELECT * FROM file_uploads;")

        query_results = cur.fetchall()

        rows = []
        for i in query_results:
            rows.append({
                "file_id": i[3],
                "file_name": i[0],
                "file_data": str(bytes(i[1]))
            })

        print(rows)
        cur.close() 
        conn.close()

        return jsonify(rows)

        # except Exception as ex:
        #     print("Failed to insert file into db")

        #     return "FAILED"

        

    return app