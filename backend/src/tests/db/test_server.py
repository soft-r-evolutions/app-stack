from app_stack.db.server import Server

TEST_DB_NAME = "testDatabase"

def get_server_connection():
    server = Server()
    server.connect()
    return server

class TestClass():
    def setup_class(self):
        print("setup_class called once for the class")
        server = get_server_connection()
        dbs = server.get_database_names()
        if TEST_DB_NAME in dbs:
            server.drop_db(database=TEST_DB_NAME)

    def teardown_class(self):
        print("teardown_class called once for the class")

    def setup_method(self):
        print("  setup_method called for every method")

    def teardown_method(self):
        print("  teardown_method called for every method")

    def test_connect(self):
        server = Server()
        assert server.connect()
        assert server.is_connected()

    def test_invalid_connect(self):
        invalid_uri = "mongodb://invalid_mongo"
        server = Server(server_uri=invalid_uri)
        assert not server.connect()
        assert not server.is_connected()

    def test_get_database_names(self):
        server = get_server_connection()
        dbs = server.get_database_names()
        assert len(dbs) > 1

    def test_db(self):
        server = get_server_connection()
        dbs = server.get_database_names()
        assert not TEST_DB_NAME in dbs

        server.create_db(database=TEST_DB_NAME)
        dbs = server.get_database_names()
        assert TEST_DB_NAME in dbs

        server.drop_db(database=TEST_DB_NAME)
        dbs = server.get_database_names()
        assert not TEST_DB_NAME in dbs
