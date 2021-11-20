from CONSTANTS import courses, subjects, groups
from student_db import engine, Course, Group, Students, Timetable
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker
from random import choice


session = sessionmaker(bind=engine)()
fkr = Faker()


def save_to_db(obj):
    session.add(obj)
    session.commit()


def create_student(student_count=1):
    for i in range(student_count):
        name = 'James Schultz'
        email = "andriitccnt@gmail.com"
        student = Students(student_name=name, student_email=email, group_id=1, course_id=1)
        save_to_db(student)


def create_course(course_count=1):
    for i in range(course_count):
        name = choice(courses)
        course = Course(name=name)
        save_to_db(course)


def create_group(group_count=1):
    for i in range(group_count):
        name = choice(groups)
        group = Group(name=name, course_id=1)
        save_to_db(group)


def gen_subject():
    return choice(subjects)


def single_day_timetable():

    daily_timetable = f'1 : {gen_subject()}, 2 : {gen_subject()}, 3: {gen_subject()}, 4 : {gen_subject()}'

    return daily_timetable


def weekly_timetable():
    mon = single_day_timetable()
    tue = single_day_timetable()
    wed = single_day_timetable()
    thu = single_day_timetable()
    fri = single_day_timetable()
    timetable = Timetable(monday=mon, tuesday=tue, wednesday=wed, thursday=thu, friday=fri, group_id=1)
    save_to_db(timetable)


#create_course()
#create_group()
#create_student()
#weekly_timetable()


def get_table():
    with Session(engine) as sess:
        student = sess.query(Group).where(Students.student_name == "James Schultz").join(Students)
        result = sess.execute(student)
        for obj in result.scalars():
            return print(obj.timetable.__dict__)





















