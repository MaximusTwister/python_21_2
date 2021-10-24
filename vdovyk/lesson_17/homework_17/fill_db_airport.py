import random

from faker import Faker
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from constants import (
    AIRPLANES_NAME,
    CABIN_CLASSES,
    TYPE_OF_TICKETS,
    FLIGHT_TYPES
)
from homework_17_ArtemV import (
    Airplanes,
    Passengers,
    Tickets,
    db_engine
)

fkr = Faker()
session = sessionmaker(bind=db_engine)()


def get_random_id(table):
    id_index = 0

    ids = {'airplanes': Airplanes.airplane_id,
           'tickets': Tickets.ticket_id,
           'passengers': Passengers.passenger_id}

    table_id_field = ids.get(table.__tablename__)
    table_ids = session.query(table_id_field).all()
    return random.choice(table_ids)[id_index]


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
        price = random.randint(50, 1500)
        ticket = Tickets(type_of_ticket=type_of_ticket,
                         cabin_class=cabin_class,
                         price=price,
                         airplane_id=get_random_id(Airplanes),
                         passenger_id=get_random_id(Passengers))
        save_to_db(ticket)


def create_airplane(airplane_number=1):
    for _ in range(airplane_number):
        airplane_name = random.choice(AIRPLANES_NAME)
        flight_type = random.choice(FLIGHT_TYPES)
        quantity_seats = random.randint(100, 330)
        airplane = Airplanes(airplane_name=airplane_name,
                             flight_type=flight_type,
                             quantity_seats=quantity_seats)
        save_to_db(airplane)


def save_to_db(obj):
    session.add(obj)   # Save customer to own memory
    session.commit()   # Transaction to DB


CREATE_FLAG = False
if CREATE_FLAG:
    create_airplane(1)
    create_passenger(5)
    create_ticket(50)

    session.close()


def showcase():
    airplanes = session.query(Airplanes).all()
    [print(airplane) for airplane in airplanes]

    airplanes = session.query(Airplanes).filter(Airplanes.quantity_seats > 200)

    print(session.query(Airplanes).filter(Airplanes.quantity_seats > 200).count())
    print(session.query(Airplanes).filter(
        and_(Airplanes.quantity_seats > 200, Airplanes.flight_types != 'long-haul flight')).count())

    try:
        tickets = session.query(Airplanes).filter(Airplanes.quantity_seats > 200).first().tickets
        print([ticket.departure_time.timetuple()[:2] for ticket in tickets])
        print([ticket.departure_time.strftime('%B %Y') for ticket in tickets])
    except AttributeError:
        pass

    query = session.query(Airplanes).join(Tickets)
    for row in query:
        row: Airplanes
        print(row.tickets)




