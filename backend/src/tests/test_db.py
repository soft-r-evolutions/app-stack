from rest_example.db import Db

TEST_DB_NAME = "testDatabase"

def test_connect():
    db = Db()
    assert db.connect()

def test_invalid_connect():
    invalid_uri = "mongodb://invalid_mongo"
    db = Db(server_uri=invalid_uri)
    assert not db.connect()
