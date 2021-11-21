import random
from faker import Faker
from sqlalchemy.orm import sessionmaker

from postgres_infro import (
    db_engine,
    Students,
    Teachers,
    Audiences,
    Groups,
    Lectures
)

fkr = Faker()
session = sessionmaker(bind=db_engine)()

group_number = 5
teacher_number = 5
audience_number = 20
lecture_names = ["Information Technology Program L2",
                 "Logic Design(Digital Hardware",
                 "Object Oriented Programming",
                 "Disc. Math",
                 "Professional Ethics",
                 "Probabilities & Statistics",
                 "Principles of Manag."]
lecture_days = ["monday", "tuesday", "wednesday", "thursday", "Friday"]


def create_student(student_num=15):
    for _ in range(student_num):
        name = fkr.name()
        email = fkr.email()
        group_id = random.randint(1, group_number)
        student = Students(student_name=name, email=email, group_id=group_id)
        save_to_db(student)


def create_teacher(teacher_num=5):
    for _ in range(teacher_num):
        name = fkr.name()
        teacher = Teachers(teacher_name=name)
        save_to_db(teacher)


def create_audience(audience_num=20):
    for i in range(audience_num):
        room_number = 100 + i
        audience = Audiences(room_number=room_number)
        save_to_db(audience)


def create_group(group_num=5):
    for i in range(group_num):
        name = f"IT-{i+1}"
        group = Groups(group_name=name)
        save_to_db(group)


def create_lecture(lecture_num=5):
    for _ in range(lecture_num):
        name = random.choice(lecture_names)
        audience_id = random.randint(1, audience_number)
        group_id = random.randint(1, group_number)
        teacher_id = random.randint(1, teacher_number)
        lecture_day = random.choice(lecture_days)
        lecture = Lectures(lecture_name=name,
                           audience_id=audience_id,
                           group_id=group_id,
                           teacher_id=teacher_id,
                           lecture_day=lecture_day)
        save_to_db(lecture)


def save_to_db(obj):
    session.add(obj)
    session.commit()


def fill_db():
    create_group()
    create_teacher()
    create_student()
    create_audience()
    create_lecture()
