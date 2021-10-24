from cerberus import Validator
from pymongo.errors import DuplicateKeyError

from mongo_infra import ac_coll, flights_coll
from utils import (
    to_date,
    get_hex_code,
    query_ac,
    query_price,
    query_flight_airport
) 

flight_schema = {
    "from": {"type": "string", "required": True},
    "to": {"type": "string", "required": True},
    "eft": {"type": "integer", "required": True},
    "price": {"type": "number", "required": True},
    "ac": {"type": "string", "required": True, "allowed": query_ac()},
}

ac_schema = {
    "name": {"type": "string", "required": True},
    "manufacturer": {"type": "string", "required": True},
    "made_date": {"type": "datetime", "required": True, 'coerce': to_date},
    "capacity": {"type": "integer", "required": True},
    "hex_code": {"type": "string", "required": True, "default": get_hex_code()},
}

ticket_schema = {
    'passenger_name': {'type': 'string', 'required': True},
    'from': {'type': 'string', 'required': True, 'allowed': query_flight_airport('from')},
    'to': {'type': 'string', 'required': True, 'allowed': query_flight_airport('to')},
    'boarding_time': {'type': 'datetime', 'required': True},
    'arrival_time': {'type': 'datetime', 'required': True},
    'price': {'type': 'number', 'required': True, 'allowed': query_price()},
    'ac': {'type': 'string', 'required': True, 'allowed': query_ac()},
    'gate': {'type': 'integer', 'required': True},
    'seat': {'type': 'string', 'required': True},
}


schema_collection_mapping = {
    'ac': (ac_schema, ac_coll),
    'flight': (flight_schema, flights_coll)
}


def validate_data(document, schema):
    normalized_document = document
    validator = Validator(schema, purge_unknown=True)
    validator.validate(document)
    if not validator.errors:
        normalized_document = validator.normalized(document)
    return normalized_document, validator.errors


def save_to_db(collection, normalized_document):
    try:
        collection.insert_one(normalized_document)
        status_code, error = 200, []
    except DuplicateKeyError as duplicate_error:
        print(f'Duplicate Key Error: {duplicate_error}')
        status_code, error = 422, [str(duplicate_error)]
    return status_code, error


def validate_and_save(json_object, object_type):  # 'ac', 'flight'
    schema, collection = schema_collection_mapping.get(object_type, [None, None])
    if not all([schema, collection]):
        return False
    normalized_document, validation_errors = validate_data(document=json_object, schema=schema)
    if not validation_errors:
        print(f'Validation Successful: {normalized_document}')
        status_code, errors = save_to_db(collection=collection, normalized_document=normalized_document)
    else:
        print(f'Validation Error: {validation_errors}')
        status_code, errors = 422, validation_errors

    return status_code, errors
