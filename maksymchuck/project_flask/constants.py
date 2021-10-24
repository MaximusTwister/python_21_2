from os import environ

MONGO_URL = "mongodb+srv://levelup:levelup@cluster0.2i8of.mongodb.net"
SECRET_KEY = environ.get('FLASK_SECRET_KEY')
