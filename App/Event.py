from uuid import UUID
import bson
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os
import json

app = Flask(__name__)
CORS(app)

host = os.environ.get("MONGO_HOST", "localhost")
port = int(os.environ.get("MONGO_PORT", 27017))

client = MongoClient(host, port)

db = client[os.environ.get("MONGO_DB", 'mayaprotect')]

col = db['hives']

@cross_origin()
@app.route('/hives/<hive_id>/events', methods=['PUT'])
def update_hive_event(hive_id):
    data = request.get_json()
    update_selector = {'uuid': bson.Binary.from_uuid(UUID(hive_id))}
    update_data = {'$push': {'events': [data]}}
    try:
        result = col.update_one(update_selector, update_data)
        if (result is None):
            message = {'message': 'Hive not found', 'status': 404}
            return Response(json.dumps(message), status=404)
        return Response(status=201)
    except Exception as e:
        message = {'message': 'Error updating hive, ' + str(e), 'status': 500}
        return Response(json.dumps(message), status=500)


app.run(host="0.0.0.0", port=8080, debug=True)
