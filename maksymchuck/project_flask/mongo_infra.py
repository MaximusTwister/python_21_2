import ssl

from pymongo import MongoClient
from pymongo.collection import Collection

from constants import MONGO_URL

mongo_client = MongoClient(MONGO_URL, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)

db = mongo_client['travel']

airports_coll: Collection = db.airports
flights_coll: Collection = db.flights
ac_coll: Collection = db.ac
tickets_coll: Collection = db.tickets
users_coll: Collection = db.users

airports_coll.create_index('icao', unique=True)
ac_coll.create_index('hex_code', unique=True)
