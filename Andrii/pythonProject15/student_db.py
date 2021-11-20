
from CONSTANTS import PSQL_USER, PSQL_PASSWORD, HOST
from sqlalchemy import create_engine, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database


engine = create_engine(f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{HOST}/students_db')
Base = declarative_base()


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    groups = relationship('Group', backref='Course')


class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(120), unique=True, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    timetable = relationship('Timetable', backref='Group', uselist=False)
    students = relationship('Students', backref='Group')


class Students(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    student_name = Column(String(120), nullable=False)
    student_email = Column(String(120), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))



class Timetable(Base):
    __tablename__ = 'Timetables'
    id = Column(Integer, primary_key=True)
    monday = Column(String(200), nullable=False)
    tuesday = Column(String(200), nullable=False)
    wednesday = Column(String(200), nullable=False)
    thursday = Column(String(200), nullable=False)
    friday = Column(String(200), nullable=False)
    group_id = Column(Integer, ForeignKey('groups.id'))

if not database_exists(engine.url):
    create_database(engine.url)

#Base.metadata.create_all(engine)
#Base.metadata.drop_all(engine)