from rest_example.db import Db

def test_connect():
    db = Db()
    assert db.connect()

def test_toto():
    assert True

