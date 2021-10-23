from datetime import datetime
from random import getrandbits

from mongo_infro import (
    ac_coll,
    flights_coll,
)


def get_ac():
    ac_cursor = ac_coll.find({}, {'_id': 0, 'name': 1})
    ac = set([ac['name'] for ac in ac_cursor])
    print(f'ACs from collection: {ac}')
    return ac


def to_date(date):
    if isinstance(date, str):
        return datetime.strptime(date, '%d-%m-%Y')
    return date


def get_hex_code():
    return str(hex(getrandbits(24)))


# New
def get_flight_from():
    flight_from_cursor = flights_coll.fing({}, {'_id': 0, 'from': 1})
    flight_from = set([flight_from['from'] for flight_from in flight_from_cursor])
    return flight_from


# New
def get_flight_to():
    flight_to_cursor = flights_coll.fing({}, {'_id': 0, 'to': 1})
    flight_to = set([flight_to['to'] for flight_to in flight_to_cursor])
    return flight_to


# New
def get_price():
    price_cursor = flights_coll.fing({}, {'_id': 0, 'price': 1})
    price = set([price['price'] for price in price_cursor])
    return price


# New
def get_flights():
    flights_cursor = flights_coll.find().pretty()
    flights = set([flights for flights in flights_cursor])
    return flights
