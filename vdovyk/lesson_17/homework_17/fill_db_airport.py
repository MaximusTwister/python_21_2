import random

from faker import Faker
from sqlalchemy.orm import sessionmaker

from constants import AIRPLANES_NAME
from constants import CABIN_CLASSES
from constants import FLIGHT_TYPES
from constants import TYPE_OF_TICKETS
from homework_17_ArtemV import Airplanes
from homework_17_ArtemV import PassengerTicketAirplane
from homework_17_ArtemV import Passengers
from homework_17_ArtemV import Tickets
from homework_17_ArtemV import db_engine

fkr = Faker()
session = sessionmaker(bind=db_engine)()


def create_passenger(passenger_number=1):
    for _ in range(passenger_number):
        name = fkr.name()
        email = fkr.email()
        phone = fkr.msisdn()
        passenger = Passengers(passenger_name=name, email=email, phone=phone)
        save_to_db(passenger)


def create_ticket(ticket_number=1):
    for _ in range(ticket_number):
        type_of_ticket = random.choice(TYPE_OF_TICKETS)
        cabin_class = random.choice(CABIN_CLASSES)
        price = random.randint(5, 1500)
        ticket = Tickets(type_of_ticket=type_of_ticket,
                         cabin_class=cabin_class,
                         price=price)
        save_to_db(ticket)


def create_airplane(airplane_number=1):
    for _ in range(airplane_number):
        airplane_name = random.choice(AIRPLANES_NAME)
        flight_types = random.choice(FLIGHT_TYPES)
        quantity_seats = random.randint(100, 330)
        airplane = Airplanes(airplane_name=airplane_name,
                             flight_types=flight_types,
                             quantity_seats=quantity_seats)
        save_to_db(airplane)


def create_passenger_ticket_airplane(passenger_number, ticket_number, num=1):
    for _ in range(num):
        passenger_id = random.randint(1, passenger_number)
        ticket_id = random.randint(1, ticket_number)
        pas_tick_air = PassengerTicketAirplane(passenger_id=passenger_id,
                                               ticket_id=ticket_id)
        save_to_db(pas_tick_air)


def save_to_db(obj):
    session.add(obj)   # Save customer to own memory
    session.commit()   # Transaction to DB


create_airplane(5)
create_ticket(5)
create_passenger(5)
create_passenger_ticket_airplane(5, 5, 5)





