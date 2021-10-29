from flask_restful import fields, reqparse


flight_parser = reqparse.RequestParser()
flight_parser.add_argument('from', type=str, help="Departure Airport")
flight_parser.add_argument('to', type=str, help="Arrival Airport")
flight_parser.add_argument('ac', type=str, help="Aircraft type Error: {error_msg}")
flight_parser.add_argument('company',
                           type=str,
                           choices=('Dnipro', 'Dnipro-2'),
                           case_sensitive=False,
                           help="Avia Provider Error: {error_msg}")

flight_template = {
    "name": fields.Integer,
    "email": fields.String,
    'dob': fields.DateTime(),
}
