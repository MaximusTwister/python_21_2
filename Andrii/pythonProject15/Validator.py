
from flask_restful import reqparse, fields

student_parser = reqparse.RequestParser()

new_student_parser = reqparse.RequestParser()

subject_parser = reqparse.RequestParser()


def int_check(data):

    if isinstance(data ,str):
        return data
    else:
        raise TypeError(f'Wrong type {type(data)}')



student_parser.add_argument('student_name', type=int_check,
                            required=True,
                            help='Students name:{error_msg}')

new_student_parser.add_argument('student_name', type=int_check,
                            required=True,
                            help='Students name:{error_msg}')

new_student_parser.add_argument('student_email', type=int_check, help='Students email:{error_msg}')


new_student_parser.add_argument('course_id', type=int,  help='Students course:{error_msg}' )


new_student_parser.add_argument('group_id', type=int,  help='Students group:{error_msg}' )


subject_parser.add_argument('name', type=int_check,
                            required=True,
                            help='Subject name:{error_msg}')

subject_parser.add_argument('Subject', type=int_check,
                            required=True,
                            help='Subject coruse:{error_msg}')

student_template = {
    'student_name': fields.String,
    'student_email': fields.String,
    'group_id': fields.Integer,
    'course_id': fields.Integer,

}

timetable_template = {'monday': fields.String, 'tuesday': fields.String,
                      'wednesday': fields.String, 'thursday':fields.String,
                      'friday': fields.String, 'group_id': fields.Integer
                      }




