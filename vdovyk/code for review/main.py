from datetime import datetime
from flask import Flask, request
from flask_restful import Api, Resource, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from apscheduler.schedulers.background import BackgroundScheduler

from constants import (
    SECRET_KEY,
    PSQL_USER,
    PSQL_PASSWORD,
    HOST,
    MAIL_USERNAME,
    MAIL_DEFAULT_SENDER,
    MAIL_PASSWORD)
from validator import (
    audience_template,
    teacher_template,
    student_template,
    group_template,
    lecture_template,
    audience_parser,
    teacher_parser,
    student_parser,
    group_parser,
    lecture_parser
)
from postgres_infro import (
    init_db,
    Students,
    Groups,
    Audiences,
    Teachers,
    Lectures
)
from utils import (
    get_one_student,
    get_lectures_for_group,
    get_all_students,
    get_all_lectures,
    get_one_audience,
    get_one_teacher,
    get_one_group,
    get_one_lecture
)
from fill_db import fill_db


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{HOST}/university"
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = MAIL_USERNAME
app.config['MAIL_DEFAULT_SENDER'] = MAIL_DEFAULT_SENDER
app.config['MAIL_PASSWORD'] = MAIL_PASSWORD

db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)
mail = Mail(app)

init_db()
fill_db()


def send_email():
    students = get_all_students()
    lectures = get_all_lectures()

    days = {"0": "monday", "1": "tuesday", "2": "wednesday", "3": "thursday", "4": "Friday"}
    day = days[str(datetime.weekday(datetime.now()))]

    for student in students:
        msg = Message(f"Schedule for today", recipients=[student["email"]])
        lectures_list = []
        for lecture in lectures:
            if lecture["group_id"] == student["group_id"] and lecture["lecture_day"] == day:
                lectures_list.append(lecture)
        msg.body = f"{lectures_list}"
        mail.send(msg)


scheduler = BackgroundScheduler()
job = scheduler.add_job(func=send_email, trigger='interval', days=1, next_run_time=datetime.now())


class StudentSchedule(Resource):
    def get(self, student_id):
        lectures = get_lectures_for_group(student_id)
        result = {}
        for lecture in lectures:
            result.setdefault(lecture["lecture_day"], []).append(lecture)
        return result


class University(Resource):
    def get(self):
        audiences = Audiences.query.all()
        teachers = Teachers.query.all()
        students = Students.query.all()
        groups = Groups.query.all()
        lectures = Lectures.query.all()
        results = [
            {"audiences": [{"audience_id": audience.audience_id,
                            "room_number": audience.room_number
                            } for audience in audiences]},

            {"teachers": [{"teacher_id": teacher.teacher_id,
                           "teacher_name": teacher.teacher_name
                           } for teacher in teachers]},

            {"students": [{"students_id": student.student_id,
                           "students_name": student.student_name,
                           "email": student.email,
                           "group_id": student.group_id,
                           } for student in students]},

            {"groups": [{"group_id": group.group_id,
                         "group_name": group.group_name,
                         } for group in groups]},

            {"lectures": [{"lecture_id": lecture.lecture_id,
                           "lecture_name": lecture.lecture_name,
                           "audience_id": lecture.audience_id,
                           "group_id": lecture.group_id,
                           "teacher_id": lecture.teacher_id,
                           "lecture_day": lecture.lecture_day
                           } for lecture in lectures]}
        ]
        return results


class AudiencesList(Resource):
    @marshal_with(audience_template)
    def get(self):
        audiences = Audiences.query.all()
        return audiences

    def post(self):
        if request.is_json:
            data = audience_parser.parse_args()
            new_audience = Audiences(room_number=data["room_number"])
            db.session.add(new_audience)
            db.session.commit()
            return {"message": f"Audience {new_audience.room_number} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


class Audience(Resource):
    @marshal_with(audience_template)
    def get(self, audience_id):
        audience = list(Audiences.query.filter(Audiences.audience_id == audience_id))
        return audience

    def put(self, audience_id):
        if request.is_json:
            data = audience_parser.parse_args()
            db.session.query(Audiences).filter(Audiences.audience_id == audience_id).update(
                {"room_number": data["room_number"]}, synchronize_session="fetch")
            db.session.commit()
            return {"message": f"Audience {data['room_number']} successfully updated"}
        else:
            return {"error": "The request payload is not in JSON format"}

    def delete(self, audience_id):
        room_number = get_one_audience(audience_id)[0]["room_number"]
        db.session.query(Audiences).filter(Audiences.audience_id == audience_id).delete()
        db.session.commit()
        return {"message": f"Audience {room_number} successfully deleted"}


class TeachersList(Resource):
    @marshal_with(teacher_template)
    def get(self):
        teachers = Teachers.query.all()
        return teachers

    def post(self):
        if request.is_json:
            data = teacher_parser.parse_args()
            new_teacher = Teachers(teacher_name=data["teacher_name"])
            db.session.add(new_teacher)
            db.session.commit()
            return {"message": f"Teacher {new_teacher.teacher_name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


class Teacher(Resource):
    @marshal_with(teacher_template)
    def get(self, teacher_id):
        teacher = list(Teachers.query.filter(Teachers.teacher_id == teacher_id))
        return teacher

    def put(self, teacher_id):
        if request.is_json:
            data = teacher_parser.parse_args()
            db.session.query(Teachers).filter(Teachers.teacher_id == teacher_id).update(
                {"teacher_name": data["teacher_name"]}, synchronize_session="fetch")
            db.session.commit()
            return {"message": f"Teacher {data['teacher_name']} successfully updated"}
        else:
            return {"error": "The request payload is not in JSON format"}

    def delete(self, teacher_id):
        teacher_name = get_one_teacher(teacher_id)[0]["teacher_name"]
        db.session.query(Teachers).filter(Teachers.teacher_id == teacher_id).delete()
        db.session.commit()
        return {"message": f"Teacher {teacher_name} successfully deleted"}


class StudentsList(Resource):
    @marshal_with(student_template)
    def get(self):
        students = Students.query.all()
        return students

    def post(self):
        if request.is_json:
            data = student_parser.parse_args()
            new_student = Students(student_name=data["student_name"],
                                   email=data["email"],
                                   group_name=data["group_id"])
            db.session.add(new_student)
            db.session.commit()
            return {"message": f"Student {new_student.student_name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


class Student(Resource):
    @marshal_with(student_template)
    def get(self, student_id):
        student = list(Students.query.filter(Students.student_id == student_id))
        return student

    def put(self, student_id):
        if request.is_json:
            data = student_parser.parse_args()
            db.session.query(Students).filter(Students.student_id == student_id).update(
                {"students_name": data["students_name"],
                 "email": data["email"],
                 "group_id": data["group_id"],
                 }, synchronize_session="fetch")
            db.session.commit()
            return {"message": f"Student {data['students_name']} successfully updated"}
        else:
            return {"error": "The request payload is not in JSON format"}

    def delete(self, student_id):
        student_name = get_one_student(student_id)[0]["student_name"]
        db.session.query(Students).filter(Students.student_id == student_id).delete()
        db.session.commit()
        return {"message": f"Student {student_name} successfully deleted"}


class GroupsList(Resource):
    @marshal_with(group_template)
    def get(self):
        groups = Groups.query.all()
        return groups

    def post(self):
        if request.is_json:
            data = group_parser.parse_args()
            new_group = Groups(group_name=data["group_name"])
            db.session.add(new_group)
            db.session.commit()
            return {"message": f"Group {new_group.group_name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


class Group(Resource):
    @marshal_with(group_template)
    def get(self, group_id):
        group = list(Groups.query.filter(Groups.group_id == group_id))
        return group

    def put(self, group_id):
        if request.is_json:
            data = group_parser.parse_args()
            db.session.query(Groups).filter(Groups.group_id == group_id).update(
                {"group_name": data["group_name"]}, synchronize_session="fetch")
            db.session.commit()
            return {"message": f"Group {data['group_name']} successfully updated"}
        else:
            return {"error": "The request payload is not in JSON format"}

    def delete(self, group_id):
        group_name = get_one_group(group_id)[0]["group_name"]
        db.session.query(Groups).filter(Groups.group_id == group_id).delete()
        db.session.commit()
        return {"message": f"Group {group_name} successfully deleted"}


class LecturesList(Resource):
    @marshal_with(lecture_template)
    def get(self):
        lectures = Lectures.query.all()
        return lectures

    def post(self):
        if request.is_json:
            data = lecture_parser.parse_args()
            new_lecture = Lectures(lecture_name=data["lecture_name"],
                                   audience_id=data["audience_id"],
                                   group_id=data["group_id"],
                                   teacher_id=data["teacher_id"],
                                   lecture_date=data["lecture_day"],)
            db.session.add(new_lecture)
            db.session.commit()
            return {"message": f"Lecture {new_lecture.lecture_name} has been created successfully."}
        else:
            return {"error": "The request payload is not in JSON format"}


class Lecture(Resource):
    @marshal_with(lecture_template)
    def get(self, lecture_id):
        lecture = list(Lectures.query.filter(Lectures.lecture_id == lecture_id))
        return lecture

    def put(self, lecture_id):
        if request.is_json:
            data = lecture_parser.parse_args()
            db.session.query(Lectures).filter(Lectures.lecture_id == lecture_id).update(
                {"lecture_name": data["lecture_name"],
                 "audience_id": data["audience_id"],
                 "group_id": data["group_id"],
                 "teacher_id": data["teacher_id"],
                 "lecture_day": data["lecture_day"],
                 }, synchronize_session="fetch")
            db.session.commit()
            return {"message": f"Lecture {data['lecture_name']} successfully updated"}
        else:
            return {"error": "The request payload is not in JSON format"}

    def delete(self, lecture_id):
        lecture_name = get_one_lecture(lecture_id)[0]["lecture_name"]
        db.session.query(Lectures).filter(Lectures.lecture_id == lecture_id).delete()
        db.session.commit()
        return {"message": f"Lecture {lecture_name} successfully deleted"}


api.add_resource(University, "/university")
api.add_resource(AudiencesList, "/university/audiences")
api.add_resource(Audience, "/university/audience/<int:audience_id>")
api.add_resource(TeachersList, "/university/teachers")
api.add_resource(Teacher, "/university/teacher/<int:teacher_id>")
api.add_resource(StudentsList, "/university/students")
api.add_resource(Student, "/university/student/<int:student_id>")
api.add_resource(GroupsList, "/university/groups")
api.add_resource(Group, "/university/group/<int:group_id>")
api.add_resource(LecturesList, "/university/lectures")
api.add_resource(Lecture, "/university/lecture/<int:lecture_id>")
api.add_resource(StudentSchedule, "/university/schedule/<int:student_id>")


if __name__ == '__main__':
    app.run(debug=True)
