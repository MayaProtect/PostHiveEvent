import unittest
import docker
import pymongo
import time
from uuid import UUID
from colorama import Fore

from App import Event


class TestEvent(unittest.TestCase):
    def setUp(self):
        # create params
        params = {
            'mongo_host': 'localhost',
            'mongo_port': 27018,
            'mongo_db': 'mayaprotect'
        }

        # Create mongo
        self.mongo_client = pymongo.MongoClient(params['mongo_host'], params['mongo_port'])
        print(str(self.mongo_client.list_database_names()))
        self.mongo_db = self.mongo_client[params['mongo_db']]
        print(Fore.GREEN + str(self.mongo_db.list_collection_names()) + Fore.RESET)

        # Get first hive id
        self.hive_id = UUID(bytes=(self.mongo_db['hives'].find_one({})['uuid']))

        self.data_test = {
            'eventType': 'test',
            'description': 'test'
        }

    def test_constructor(self):

        print(str(self.hive_id))
        # create event
        self.event = Event(self.data_test, self.hive_id, self.mongo_db)

        # check if event is created
        self.assertIsInstance(self.event, Event)


    def test_event_hive_id_raise_type_error(self):
        # create event
        with self.assertRaises(TypeError):
            self.event = Event(self.data_test, 'test', self.mongo_db)

    def test_event_db_raise_type_error(self):
        # create event
        with self.assertRaises(TypeError):
            self.event = Event(self.data_test, self.hive_id, 'test')

    def test_event_data_raise_type_error(self):
        # create event
        with self.assertRaises(TypeError):
            self.event = Event('test', self.hive_id, self.mongo_db)

    def test_event_data_raise_value_error(self):
        # create event
        with self.assertRaises(ValueError):
            self.event = Event({'eventType': '', 'description': ''}, self.hive_id, self.mongo_db)

    def test_event_data_event_type_raise_value_error(self):
        # create event
        with self.assertRaises(ValueError):
            self.event = Event({'eventType': 'test', 'description': ''}, self.hive_id, self.mongo_db)

    def test_event_data_description_raise_value_error(self):
        # create event
        with self.assertRaises(ValueError):
            self.event = Event({'eventType': '', 'description': 'test'}, self.hive_id, self.mongo_db)

    def test_event_data_event_type_raise_type_error(self):
        # create event
        with self.assertRaises(TypeError):
            self.event = Event({'eventType': 1, 'description': 'test'}, self.hive_id, self.mongo_db)

    def test_event_data_description_raise_type_error(self):
        # create event
        with self.assertRaises(TypeError):
            self.event = Event({'eventType': 'test', 'description': 1}, self.hive_id, self.mongo_db)

    def test_to_dict(self):
        # create event
        self.event = Event(self.data_test, self.hive_id, self.mongo_db)

        # check if event is created
        self.assertIsInstance(self.event.to_dict(), dict)
        self.assertEqual(self.event.to_dict()['eventType'], self.data_test['eventType'])
        self.assertEqual(self.event.to_dict()['description'], self.data_test['description'])

    def test_to_response(self):
        # create event
        self.event = Event(self.data_test, self.hive_id, self.mongo_db)

        # check if event is created
        self.assertIsInstance(self.event.to_response(), dict)
        self.assertEqual(self.event.to_response()['eventType'], self.data_test['eventType'])
        self.assertEqual(self.event.to_response()['description'], self.data_test['description'])
    
    @classmethod
    def setUpClass(cls):
        # Start docker mongo container
        print(Fore.BLUE + 'Starting docker containers...' + Fore.RESET)
        cls.client = docker.from_env()
        cls.container = cls.client.containers.run('mongo', detach=True, ports={'27017/tcp': 27018}, name='testmongo', network='bridge')
        cls.container_id = cls.container.id
        print(Fore.BLUE + 'Docker mongo container started' + Fore.RESET)
        time.sleep(5)

        # start metricsfaker container
        cls.metricsfaker = cls.client.containers.run('pfontaine/metricsfaker', detach=True, environment={'MONGO_HOST': 'testmongo', 'MONGO_PORT': '27018', 'MONGO_DB': 'mayaprotect', 'MAX_OWNER': '1', 'MIN_OWNER': '1'}, network="bridge")
        cls.metricsfaker_id = cls.metricsfaker.id
        print(Fore.BLUE + 'Docker metricsfaker container started' + Fore.RESET)
        time.sleep(30)

        print(Fore.YELLOW + "Start tests for Event" + Fore.RESET)

    @classmethod
    def tearDownClass(cls):
        print(Fore.RED + cls.metricsfaker.logs().decode('utf-8') + Fore.RESET)
        # Stop docker containers
        print(Fore.BLUE + 'Stopping docker containers...' + Fore.RESET)
        cls.container.stop()
        cls.metricsfaker.stop()
        print(Fore.BLUE + 'Docker containers stopped' + Fore.RESET)

        # Remove docker containers
        print(Fore.BLUE + 'Removing docker containers...' + Fore.RESET)
        cls.container.remove()
        cls.metricsfaker.remove()
        print(Fore.BLUE + 'Docker containers removed' + Fore.RESET)

        print(Fore.YELLOW + "End tests for Event" + Fore.RESET)
