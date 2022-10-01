from uuid import UUID
import bson
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import os

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
    result = col.update_one(update_selector, update_data)
    return flask.Response(status=201)


app.run(host="0.0.0.0", port=8080, debug=True)
