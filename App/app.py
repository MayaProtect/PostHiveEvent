from uuid import UUID
import bson
from flask import Flask, request, Response
from flask_cors import CORS, cross_origin
from pymongo import MongoClient
import json


class PutHiveEvent:
    def __init__(self, params: dict):
        self.__mongo_host = params['mongo_host']
        self.__mongo_port = params['mongo_port']
        self.__mongo_db = params['mongo_db']
        
        self.__app = Flask(__name__)
        CORS(self.__app)
        self.__app.add_url_rule('/hives/<hive_id>/events', 'hive_event', self.__hive_event, methods=['PUT'])

        self.__mongo_client = MongoClient(self.__mongo_host, self.__mongo_port)
        self.__mongo_db = self.__mongo_client[self.__mongo_db]
    
    @cross_origin()
    def __hive_event(self, hive_id: str) -> Response:
        data = request.get_json()
        update_selector = {'uuid': bson.Binary.from_uuid(UUID(hive_id))}
        update_data = {'$push': {'events': [data]}}
        try:
            col = self.__mongo_db['hives']
            result = col.update_one(update_selector, update_data)
            if (result is None):
                message = {'message': 'Hive not found', 'status': 404}
                return Response(json.dumps(message), status=404)
            return Response(status=201)
        except Exception as e:
            message = {'message': 'Error updating hive, ' + str(e), 'status': 500}
            return Response(json.dumps(message), status=500)

    def run(self) -> None:
        self.__app.run(host='0.0.0.0', port=8080)
