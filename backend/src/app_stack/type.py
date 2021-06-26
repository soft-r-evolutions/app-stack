"""
This is the people module and supports all the ReST actions for the
PEOPLE collection
"""

# System modules
from datetime import datetime

# 3rd party modules
from flask import make_response, abort


def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


# Data to serve with our API
TYPES = [
    {
        "_id": "00000000000",
        "name": "Number",
        "version": '1',
        "collection": "primitive"
    },
    {
        "_id": "00000000001",
        "name": "String",
        "version": '1',
        "collection": "primitive"
    }
}


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    # Create the list of people from our data
    return TYPES


def read_one(name):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    # Does the person exist in people?
    result = None
    for _type in TYPES:
      if name == _type['name']:
        result = _type

    # otherwise, nope, not found
    else:
        abort(
            404, "Type with name {name} not found".format(name=name)
        )

    return result


def create(name):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    exists = False
    for _type in TYPES:
      if name == _type['name']:
        exists = True

    # Does the person exist already?
    if exists:
        TYPES.append(
        {
            "name": name,
            "collection": "{}s".format(name),
            "version": 1
        }
        return make_response(
            "{name} successfully created".format(lname=lname), 201
        )

    # Otherwise, they exist, that's an error
    else:
        abort(
            406,
            "Type with name {name} already exists".format(name=name),
        )


def update(name, updated_type):
    """
    This function updates an existing person in the people structure
    :param lname:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Does the person exist in people?
    cur_type_idx = -1
    for idx, _type in enumerate(TYPES):
      if name == _type['name']:
        cur_type_idx = idx

    if cur_type_idx != -1:
        TYPES[cur_type_idx] = updated_type

        return updated_type

    # otherwise, nope, that's an error
    else:
        abort(
            404, "Type with name {lname} not found".format(lname=lname)
        )


def delete(name):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    cur_type_idx = -1
    for idx, _type in enumerate(TYPES):
      if name == _type['name']:
        cur_type_idx = idx
    # Does the person to delete exist?

    if cur_type_idx != -1:
        del TYPES[cur_type_idx]
        return make_response(
            "{name} successfully deleted".format(name=name), 200
        )

    # Otherwise, nope, person to delete not found
    else:
        abort(
            404, "Type named {name} not found".format(name=name)
        )

