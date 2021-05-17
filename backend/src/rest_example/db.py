from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Db:
    def __init__(self):
        client = MongoClient("mongodb://mongo")
        try:
            # The ismaster command is cheap and does not require auth.
            client.admin.command('ismaster')
            dbs = client.list_database_names()
            print("list databases: {}".format(dbs))
        except ConnectionFailure:
            print("Server not available")
