from rest_example.db import Db

TEST_DB_NAME = "testDatabase"

def makeDb():
    db = Db()
    db.connect()
    return db

class TestClass():
    def setup_class(self):
        print("setup_class called once for the class")
        db = makeDb()
        dbs = db.get_database_names()
        if TEST_DB_NAME in dbs:
            db.drop_db(TEST_DB_NAME)

    def teardown_class(self):
        print("teardown_class called once for the class")

    def setup_method(self):
        print("  setup_method called for every method")

    def teardown_method(self):
        print("  teardown_method called for every method")

    def test_connect(self):
        db = Db()
        assert db.connect()

    def test_invalid_connect(self):
        invalid_uri = "mongodb://invalid_mongo"
        db = Db(server_uri=invalid_uri)
        assert not db.connect()

    def test_get_database_names(self):
        db = makeDb()
        dbs = db.get_database_names()
        assert len(dbs) > 1

    def test_db(self):
        db = makeDb()
        dbs = db.get_database_names()
        assert not TEST_DB_NAME in dbs

        db.create_db(TEST_DB_NAME)
        dbs = db.get_database_names()
        assert TEST_DB_NAME in dbs

        db.drop_db(TEST_DB_NAME)
        dbs = db.get_database_names()
        assert not TEST_DB_NAME in dbs
