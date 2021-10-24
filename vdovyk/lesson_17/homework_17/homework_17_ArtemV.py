from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Float, DateTime
from sqlalchemy_utils import create_database, database_exists

from constants import (
    HOST,
    PSQL_PASSWORD,
    PSQL_USER
)

db_name = 'airport'
db_engine = create_engine(f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{HOST}/{db_name}')
Base = declarative_base()

if not database_exists(db_engine.url):
    create_database(db_engine.url)


class Airplanes(Base):
    __tablename__ = 'airplanes'
    airplane_id = Column(Integer, primary_key=True)
    airplane_name = Column(String(100), nullable=False)
    flight_type = Column(String(100), nullable=False)
    quantity_seats = Column(Integer, nullable=False)
    tickets = relationship("Tickets", backref="airplane")

    def __str__(self):
        return f'{self.airplane_id} {self.airplane_name} {self.flight_type} {self.quantity_seats}'


class Tickets(Base):
    __tablename__ = 'tickets'
    ticket_id = Column(Integer, primary_key=True)
    airplane_id = Column(Integer, ForeignKey('airplanes.airplane_id'))
    passenger_id = Column(Integer, ForeignKey('passengers.passenger_id'))
    type_of_ticket = Column(String(100), nullable=False)
    cabin_class = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    departure_time = Column(DateTime, default=datetime.now())

    def __str__(self):
        return f'{self.ticket_id} [{self.airplane}]\n'


class Passengers(Base):
    __tablename__ = 'passengers'
    passenger_id = Column(Integer, primary_key=True)
    passenger_name = Column(String(150), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    tickets = relationship("Tickets", backref="passenger")


Base.metadata.create_all(db_engine)
