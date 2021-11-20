from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import Integer, String, Text
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import relationship, scoped_session, sessionmaker

from constants import HOST
from constants import PSQL_PASSWORD
from constants import PSQL_USER


db_engine = create_engine(f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{HOST}/university')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=db_engine))
Base = declarative_base()
Base.query = db_session.query_property()


if not database_exists(db_engine.url):
    create_database(db_engine.url)


class Students(Base):
    __tablename__ = "students"
    student_id = Column(Integer, primary_key=True)
    student_name = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    group_name = relationship("Groups", back_populates="students_")


class Groups(Base):
    __tablename__ = "groups"
    group_id = Column(Integer, primary_key=True)
    group_name = Column(String(100), unique=True, nullable=False)
    students_ = relationship("Students", back_populates="group_name")


class Audiences(Base):
    __tablename__ = "audiences"
    audience_id = Column(Integer, primary_key=True)
    room_number = Column(Integer, unique=True, nullable=False)


class Teachers(Base):
    __tablename__ = "teachers"
    teacher_id = Column(Integer, primary_key=True)
    teacher_name = Column(String(100), unique=True, nullable=False)


class Lectures(Base):
    __tablename__ = "lectures"
    lecture_id = Column(Integer, primary_key=True)
    lecture_name = Column(Text, nullable=False)
    audience_id = Column(Integer, ForeignKey("audiences.audience_id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.group_id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.teacher_id"), nullable=False)
    lecture_day = Column(String, nullable=False)


def init_db():
    Base.metadata.create_all(bind=db_engine)


init_db()
