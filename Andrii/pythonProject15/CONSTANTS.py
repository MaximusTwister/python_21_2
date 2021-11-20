

import os


PSQL_USER = os.environ['PSQL_USER']
PSQL_PASSWORD = os.environ['PSQL_PASSWORD']
HOST = 'localhost:5432'

MONGO_URL = "mongodb+srv://levelup:levelup@cluster0.2i8of.mongodb.net"


courses = ['Alchemy', 'Metaphysics', 'Sociology', 'Astronomy', 'Astrology', 'Hydromechanics', 'Computer science']
subjects = ['Taumaturgy', 'Geometry', 'Torsion fields',
            'Javascript', 'Musical theory', 'Woodworking',
            'Anatomy', 'Systems', 'Geography', 'Microbiology',
            'Group theory', 'Flow mechanics', 'Calculus'
            ]
groups = ['21_1', '21_2', '21_3', '21_4', '21_5']


timetable_test = {
    "Weekly_timetable": [
        {
            "monday": "1 : Group theory, 2 : Geometry, 3: Woodworking, 4 : Woodworking",
            "tuesday": "1 : Taumaturgy, 2 : Geography, 3: Javascript, 4 : Torsion fields",
            "wednesday": "1 : Taumaturgy, 2 : Javascript, 3: Anatomy, 4 : Microbiology",
            "thursday": "1 : Taumaturgy, 2 : Group theory, 3: Geography, 4 : Geometry",
            "friday": "1 : Group theory, 2 : Woodworking, 3: Flow mechanics, 4 : Geometry",
            "group_id": 1
        }
    ]
}
