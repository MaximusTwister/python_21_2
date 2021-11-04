import ssl

from pymongo import MongoClient     # для подключения к mongo
from pymongo.collection import Collection

from constants import MONGO_URL

mongo_client = MongoClient(MONGO_URL, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)    # ... , ssl=...для обхода ошибки с ssl

# db = mongo_client['travel']

db = mongo_client['security_db']
prehashed_collection = db.prehashed
users_coll: Collection = db.users

airports_coll: Collection = db.airports
flights_coll: Collection = db.flights
ac_coll: Collection = db.ac     # ac - aircraft
tickets_coll: Collection = db.ticket
# users_coll: Collection = db.users




# TODO with try
airports_coll.create_index('icao', unique=True)
ac_coll.create_index('hex_code', unique=True)
