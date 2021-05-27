COLLECTION_NAME = "types"

TYPE_NAME_KEY = "name"
TYPE_ID_KEY = "_id"

TYPE_VERSION_KEY = "version"
DEFAULT_TYPE_VERSION = 1

TYPE_COLLECTION_KEY = "collection"
TYPE_PRIMITIVE_VALUE = "primitive"
DEFAULT_TYPE_COLLECTION = TYPE_PRIMITIVE_VALUE

STRING_VALUE = "String"
NUMBER_VALUE = "Number"

def make_app_stack_type(type_name, **kwargs):
    app_stack_type = dict()

    app_stack_type[TYPE_NAME_KEY] = type_name 

    version = kwargs.get(TYPE_VERSION_KEY, DEFAULT_TYPE_VERSION)
    print("- {}: {}".format(TYPE_VERSION_KEY, version))
    app_stack_type[TYPE_VERSION_KEY] = version

    collection = kwargs.get(TYPE_COLLECTION_KEY, DEFAULT_TYPE_COLLECTION)
    print("- {}: {}".format(TYPE_COLLECTION_KEY, collection))
    app_stack_type[TYPE_COLLECTION_KEY] = collection

    return app_stack_type
