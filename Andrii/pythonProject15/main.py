import schedule

from Validator import student_parser,student_template, timetable_template, new_student_parser

from flask import Flask

from student_db import Students, Group, engine, Timetable

from flask_restful import Api, Resource, marshal

from sqlalchemy.orm import Session

from utils import send_email



app = Flask(__name__)
api = Api(app)

session = Session(engine)


class Student(Resource):

    def get(self):
        return {'students': [marshal(res, student_template)for res in session.query(Students).all()]}

    def post(self):
        args = student_parser.parse_args(strict=True)
        return {'students': [marshal(res, student_template)for res in
                             session.query(Students).where(Students.student_name == args["student_name"])]}


class Timetables(Resource):

    def get(self):

        return {'Weekly_timetable': [marshal(res, timetable_template)for res in session.query(Timetable).all()] }

    def post(self):
        with Session(engine) as sess:
            args = student_parser.parse_args(strict=True)
            student = sess.query(Group).where(Students.student_name == args["student_name"]).join(Students)
            result = sess.execute(student)
            for obj in result.scalars():
                return marshal(obj.timetable, timetable_template)


class NewStudent(Resource):

    def post(self):
        with Session(engine) as sess:
            args = new_student_parser.parse_args(strict=True)
            name = args['student_name']
            email = args['student_email']
            group = args['group_id']
            course = args['course_id']
            student = Students(student_name=name, student_email=email, group_id=group, course_id=course)
            sess.add(student)
            sess.commit()
            return "Saved"


def table_emailer():
    table = marshal(session.query(Timetable), timetable_template)
    emails = marshal(session.query(Students.student_email).all(), student_template)
    mail_list = [x["student_email"] for x in emails]
    for e in mail_list:
        send_email(table, e)


schedule.every().day.at("8:00").do(table_emailer)


api.add_resource(Student, '/', '/student')
api.add_resource(Timetables, '/timetable')
api.add_resource(NewStudent, '/new_student')


if __name__ == '__main__':
    app.run(debug=True)





