from uuid import uuid4, UUID
from datetime import datetime
from pymongo.database import Database
from bson.binary import Binary


class Event:
    def __init__(self, data: dict, hive_id: UUID, db: Database):
        if type(data) is not dict:
            raise TypeError('Invalid data')

        if type(data['description']) is not str:
            raise TypeError('Invalid description')

        if type(data['eventType']) is not str:
            raise TypeError('Invalid eventType')

        if len(data['description']) < 1:
            raise ValueError('Invalid description')

        if len(data['eventType']) < 1:
            raise ValueError('Invalid eventType')

        if type(db) is not Database:
            raise TypeError('Invalid db')

        if type(hive_id) is not UUID:
            raise TypeError('Invalid hive_id')

        self.__id = uuid4()
        self.__createdAt = datetime.now()
        self.__message = data['description']
        self.__event_type = data['eventType']
        self.owner = self.__get_owner(hive_id, db)

    def to_dict(self) -> dict:
        return {
            'uuid': Binary.from_uuid(self.__id),
            'createdAt': str(self.__createdAt),
            'description': self.__message,
            'eventType': self.__event_type,
            'owner': self.__owner_to_dict(self.owner)
        }

    def to_response(self) -> dict:
        return {
            'uuid': str(self.__id),
            'createdAt': str(self.__createdAt),
            'description': self.__message,
            'eventType': self.__event_type,
            'owner': self.__owner_to_response(self.owner)
        }

    def __get_owner(self, hive_id: UUID, db: Database) -> str:
        col = db['hives']
        result = col.find_one({'uuid': Binary.from_uuid(hive_id)})
        if (result is None):
            print('Hive not found')
            raise Exception('Hive not found')
        return result['owner']

    def __owner_to_dict(self, owner):
        return {
            'uuid': Binary.from_uuid(UUID(bytes=owner['uuid'])),
            'name': owner['name'] if 'name' in owner else owner['firstname'] + ' ' + owner['lastname']
        }
    
    def __owner_to_response(self, owner):
        return {
            'uuid': str(UUID(bytes=owner['uuid'])),
            'name': owner['name'] if 'name' in owner else owner['firstname'] + ' ' + owner['lastname']
        }