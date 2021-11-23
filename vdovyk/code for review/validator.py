from flask_restful import reqparse, fields


audience_parser = reqparse.RequestParser()
teacher_parser = reqparse.RequestParser()
student_parser = reqparse.RequestParser()
group_parser = reqparse.RequestParser()
lecture_parser = reqparse.RequestParser()


def strict_str_validator(data):
    if isinstance(data, str):
        return data
    else:
        raise TypeError(f"Wrong type:{type(data)}")


audience_parser.add_argument("room_number",
                             type=int,
                             required=True,
                             help="Room number: {error_msg}")

teacher_parser.add_argument("teacher_name",
                            type=strict_str_validator,
                            required=True,
                            help="Teacher's name: {error_msg}")

student_parser.add_argument("student_name",
                            type=strict_str_validator,
                            required=True,
                            help="Student's name: {error_msg}")

student_parser.add_argument("email",
                            type=strict_str_validator,
                            required=True,
                            help="Email: {error_msg}")

student_parser.add_argument("group_id",
                            type=str,
                            required=True,
                            help="Group's id: {error_msg}")

group_parser.add_argument("group_name",
                          type=str,
                          required=True,
                          help="Group's name: {error_msg}")


lecture_parser.add_argument("lecture_name",
                            type=str,
                            required=True,
                            help="Lecture's name: {error_msg}")

lecture_parser.add_argument("lecture_day",
                            type=str,
                            required=True,
                            help="Lecture's day: {error_msg}")

lecture_parser.add_argument("group_id",
                            type=int,
                            required=True,
                            help="Group id: {error_msg}")

lecture_parser.add_argument("audience_id",
                            type=int,
                            required=True,
                            help="Audience id: {error_msg}")

lecture_parser.add_argument("teacher_id",
                            type=int,
                            required=True,
                            help="Teacher id: {error_msg}")

audience_template = {
    "audience_id": fields.Integer,
    "room_number": fields.Integer,
}

teacher_template = {
    "teacher_id": fields.Integer,
    "teacher_name": fields.String,
}

student_template = {
    "student_id": fields.Integer,
    "student_name": fields.String,
    "group_id": fields.Integer,
    "email": fields.String,
}

group_template = {
    "group_id": fields.Integer,
    "group_name": fields.String,
}

lecture_template = {
    "lecture_id": fields.Integer,
    "lecture_name": fields.String,
    "audience_id": fields.Integer,
    "group_id": fields.Integer,
    "teacher_id": fields.Integer,
    "lecture_day": fields.String,
}
