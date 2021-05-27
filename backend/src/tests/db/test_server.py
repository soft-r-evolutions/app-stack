import unittest
from app_stack.db.server import Server
import app_stack.db.types as types

TEST_DB_NAME = "app_stack_test"
TMP_DB_NAME = "tmpDatabase"

module_server = Server(database=TEST_DB_NAME)

def _remove_databases():
    dbs = module_server.get_database_names()
    if TEST_DB_NAME in dbs:
        module_server.drop_db()
    if TMP_DB_NAME in dbs:
        module_server.drop_db(database=TMP_DB_NAME)

def setup_module():
    print("setup_class called once for the class")
    module_server.connect()
    print (module_server)
    _remove_databases()

def teardown_module():
    print("teardown_class called once for the class")
    _remove_databases()

def setup_function():
    print("  setup_method called for every method")
    _remove_databases()
    module_server.create_db()

def teardown_function():
    print("  teardown_method called for every method")
    _remove_databases()

def test_connect():
    server = Server()
    assert not server.is_connected()
    assert server.connect()
    assert server.is_connected()

def test_invalid_connect():
    invalid_uri = "mongodb://invalid_mongo"
    server = Server(server_uri=invalid_uri)
    assert not server.connect()
    assert not server.is_connected()

def test_get_database_names():
    dbs = module_server.get_database_names()
    assert len(dbs) > 1

def test_db():
    dbs = module_server.get_database_names()
    assert not TMP_DB_NAME in dbs

    module_server.create_db(database=TMP_DB_NAME)
    dbs = module_server.get_database_names()
    assert TMP_DB_NAME in dbs

    module_server.drop_db(database=TMP_DB_NAME)
    dbs = module_server.get_database_names()
    assert not TMP_DB_NAME in dbs

def test_get_type_list():
    dbs = module_server.get_database_names()
    print (dbs)
    type_list = module_server.get_type_list()
    print ("{}".format(type_list))

    assert len(type_list) > 1

def test_add_type():
    document = module_server.get_type_by_name("toto")
    assert not document
    module_server.add_type("toto")
    document = module_server.get_type_by_name("toto")
    print ("{}".format(document))
    assert document['name'] == "toto"

def test_find_type_by_name():
    document = module_server.get_type_by_name("toto")
    assert not document
    document = module_server.get_type_by_name(types.STRING_VALUE)
    print ("{}".format(document))
    assert document['name'] == types.STRING_VALUE

def test_find_type_by_id():
    document = module_server.get_type_by_id("toto")
    assert not document
    result = module_server.add_type("toto")
    print("toto id : {}".format(result.inserted_id))
    document = module_server.get_type_by_id(result.inserted_id)
    print ("{}".format(document))
    assert document['name'] == "toto"
    assert document['_id'] == result.inserted_id



