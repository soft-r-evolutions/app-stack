from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import app_stack.db.types as types

class Server:
    ARG_SERVER_URI_KEY = "server_uri"
    DEFAULT_SERVER_URI = "mongodb://mongo"

    ARG_DATABASE_NAME_KEY = "database"
    DEFAULT_DATABASE_NAME = "appStack"

    ARG_CREATE_OPTION_KEY = "create"
    DEFAULT_CREATE_OPTION = False

    DEFAULT_CONNECT_TIMEOUT = 2000


    def __init__(self, **kwargs):
        print("Declare MongoDb Server:")
        self.server_uri = kwargs.get(Server.ARG_SERVER_URI_KEY, Server.DEFAULT_SERVER_URI)
        print("- {}: {}".format(Server.ARG_SERVER_URI_KEY, self.server_uri))
        self.database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, Server.DEFAULT_DATABASE_NAME)
        print("- {}: {}".format(Server.ARG_DATABASE_NAME_KEY, self.database_name))
        self.create_option = kwargs.get(Server.ARG_CREATE_OPTION_KEY, Server.DEFAULT_CREATE_OPTION)
        print("- {}: {}".format(Server.ARG_CREATE_OPTION_KEY, self.create_option))

        self.client = None
        self._is_connected = False

        self.database = None


    def connect(self):
        print("Connect MongoDb Server...")
        self.client = MongoClient(self.server_uri, serverSelectionTimeoutMS=Server.DEFAULT_CONNECT_TIMEOUT)
        try:
            # The ismaster command is cheap and does not require auth.
            self.client.admin.command('ismaster')
            self._is_connected = True
            print("MongoDb Server is connected.")
            return True
        except ConnectionFailure:
            print("***** MongoDb Server is not available. *****")
            return False


    def is_connected(self):
        return self._is_connected


    def select_db(self, **kwargs):
        if not self.is_connected:
            print("***** Server must be connected to select a database. *****")
            return False

        self.database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        print("Select MongoDb Server database: {}".format(self.database_name))
        if self.exists_db(database=self.database_name):
            print("Existing MongoDb Server database: {} is now selected".format(self.database_name))
            self.database = self.client[database_name]
            return True

        create_option = kwargs.get(Server.ARG_CREATE_OPTION_KEY, self.create_option)
        if create_option:
            print("Create option detected for unexisting MongoDb Server database: {}".format(self.database_name))
            return self.create_db()

        print("Unexisting MongoDb Server database: {} can not be selected".format(self.database_name))
        return False


    def has_database_selected(self):
        if not self.is_connected:
            return False
        return True if self.database else False


    def exists_db(self, **kwargs):
        if not self.is_connected:
            print("Server must be connected to check if a database exists.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        dbs = self.get_database_names()
        return database_name in dbs


    def create_db(self, **kwargs):
        if not self.is_connected:
            print("Server must be connected to check if a database exists.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        print("Create MongoDb Server database: {}".format(database_name))
        return self.init_database(database=database_name)


    def drop_db(self, **kwargs):
        if not self.is_connected:
            print("Server must be connected to drop a database.")
            return False
        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        print("Drop MongoDb Server database: {}".format(database_name))
        self.client.drop_database(database_name)
        return True


    def get_database_names(self):
        if not self.is_connected:
            print("Server must be connected to get database list.")
            return False

        dbs = self.client.list_database_names()
        print("MongoDb Server database list: {}".format(dbs))
        return dbs


    def init_database(self, **kwargs):
        if not self.is_connected:
            print("Server must be connected to get database list.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        print("Initialize MongoDb Server database: {}".format(database_name))

        self.add_type(types.STRING_VALUE, database=database_name)
        self.add_type(types.NUMBER_VALUE, database=database_name)

        return True


    def add_type(self, type_name, **kwargs):
        if not self.is_connected:
            print("Server must be connected to add a new type.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        print("Trying to add new type {} to database: {}...".format(type_name, database_name))

        app_stack_type = types.make_app_stack_type(type_name, **kwargs)

        database = self.client[database_name]
        types_collection = database[types.COLLECTION_NAME]

        result = types_collection.insert_one(app_stack_type)
        print ("app_stack_type inserted with id: {}".format(result.inserted_id))

        return result


    def get_type_list(self, **kwargs):
        if not self.is_connected:
            print("Server must be connected to add a new type.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        database = self.client[database_name]

        types_collection = database[types.COLLECTION_NAME]

        cursor = types_collection.find({})
        print("Database {} type list:".format(database_name))
        type_list = []
        for type_document in cursor:
            type_list.append(type_document)
            # print("- {}".format(type_document))
        return type_list


    def get_type_by_name(self, type_name, **kwargs):
        if not self.is_connected:
            print("Server must be connected to add a new type.")
            return False

        database_name = kwargs.get(Server.ARG_DATABASE_NAME_KEY, self.database_name)
        database = self.client[database_name]

        types_collection = database[types.COLLECTION_NAME]

        print("Database {} - search type named: {}".format(database_name, type_name))
        type_document = types_collection.find_one({types.TYPE_NAME_KEY: type_name})
        return type_document

    def __str__(self):
        result = "Connection to: {}\n".format(self.server_uri)
        result += "- Default database: {}\n".format(self.database_name)
        is_connected_str = "CONNECTED" if self.is_connected else "NOT CONNECTED"
        result += "- State: {}\n".format(is_connected_str)
        return result
