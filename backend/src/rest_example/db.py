from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Db:
    ARG_SERVER_URI_KEY = "server_uri"
    DEFAULT_SERVER_URI = "mongodb://mongo"

    def __init__(self, **kwargs):
        self.server = kwargs.get(Db.ARG_SERVER_URI_KEY, Db.DEFAULT_SERVER_URI)

        self.client = MongoClient(self.server)

    def connect(self):
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            return True
        except ConnectionFailure:
            print("Server not available")
            return False

    def create_db(self, database_name):
        self.client[database_name]

    def drop_db(self, database_name):
        self.client.drop_database(database_name)

    def get_database_names():
        dbs = self.client.list_database_names()
        print("list databases: {}".format(dbs))
        return dbs
