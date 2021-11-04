from cerberus import Validator
from pymongo.errors import DuplicateKeyError

from mongo_infro import ac_coll, flights_coll, tickets_coll
from utils import (
    query_ac,
    to_date,
    get_hex_code,
    query_flight_airport,
    query_price,
)

flight_schema = {
    'from': {'type': 'string', 'required': True},
    'to': {'type': 'string', 'required': True},
    'eft': {'type': 'integer', 'required': True},       # estimate flight time
    'price': {'type': 'number', 'required': True},      # number -  type float
    'ac': {'type': 'string', 'required': True, 'allowed': query_ac()},    # 'allowed' - список разреженных самолетов
}

ac_schema = {
    'name': {'type': 'string', 'required': True},
    'manufacturer': {'type': 'string', 'required': True},
    'made_date': {'type': 'datetime', 'required': True, 'coerce': to_date},
    'capacity': {'type': 'integer', 'required': True},
    'hex_code': {'type': 'string', 'required': True, 'default': get_hex_code()},
}
# New
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
    'flight': (flight_schema, flights_coll),
    'ticket': (ticket_schema, tickets_coll)     # New
}


def validate_date(document, schema):
    normalized_document = document
    validator = Validator(schema, purge_unknown=True)   # создаем экземпляр класса
    validator.validate(document)
    if not validator.errors:
        normalized_document = validator.normalized(document)
    return normalized_document, validator.errors


def save_to_db(collection, normalization_document):
    try:
        collection.insert_one(normalization_document)
        status_code, errors = 200, []
    except DuplicateKeyError as duplicate_error:
        print(f'Duplicate Key Error: {duplicate_error}')
        status_code, errors = 422, [str(duplicate_error)]
    return status_code, errors


def validate_and_save(json_object, object_type):
    schema, collection = schema_collection_mapping.get(object_type, [None, None])
    if not all([schema, collection]):
        return False
    normalized_document, validation_errors = validate_date(document=json_object, schema=schema)
    if not validation_errors:
        print(f'Validation Successful: {normalized_document}')
        status_code, errors = save_to_db(collection=collection, normalization_document=normalized_document)
    else:
        print(f'Validation Error: {validation_errors}')
        status_code, errors = 422, validation_errors

    return status_code, errors
