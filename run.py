from os import environ as env
from App import PutHiveEvent

def main():
    params = {
        'mongo_host': env.get('MONGO_HOST', 'localhost'),
        'mongo_port': int(env.get('MONGO_PORT', 27017)),
        'mongo_db': env.get('MONGO_DB', 'hives')
    }
    app = PutHiveEvent(params)
    app.run()


if __name__ == '__main__':
    main()
