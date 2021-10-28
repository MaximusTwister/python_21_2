from datetime import datetime, timedelta
from random import getrandbits



import jwt

from mongo_infro import (
    ac_coll,
    flights_coll,
)


def query_ac():
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
def query_flight_airport(point):
    if point in ['from', 'to']:
        flight_point_cursor = flights_coll.find({}, {'_id': 0, point: 1})
        flight_point = set([flight_point[point] for flight_point in flight_point_cursor])
        return flight_point


# New
def query_price():
    price_cursor = flights_coll.find({}, {'_id': 0, 'price': 1})
    price = set([price['price'] for price in price_cursor])
    return price


# New
def query_flights():
    flights_cursor = flights_coll.find()
    flights = set([flights for flights in flights_cursor])
    return flights


def encode_jwt(user_id, key):
    print(f'Encode JWT: {user_id} : {key}')
    payload = {
        'exp': (datetime.utcnow() + timedelta(days=0, minutes=2)).isoformat(),      # time by grinvich
        'ist': (datetime.utcnow()).isoformat(),                                     # issue time время выпуска
        'sub': user_id,
    }
    return jwt.encode(payload, key, algorithm='HS256')


