from postgres_infro import Students, Lectures, Audiences, Teachers, Groups


def get_all_students():
    students_query = Students.query.all()
    students = [
        {
            "students_id": student.student_id,
            "students_name": student.student_name,
            "email": student.email,
            "group_id": student.group_id,
            "group": student.group_name,
        } for student in students_query]
    return students


def get_one_student(student_id):
    student_found = Students.query.filter(Students.student_id == student_id)
    result = [
        {
            "student_id": student.student_id,
            "student_name": student.student_name,
            "email": student.email,
            "group_id": student.group_id,
        } for student in student_found]
    return result


def get_all_lectures():
    lectures_query = Lectures.query.all()
    lectures = [
        {
            "lecture_id": lecture.lecture_id,
            "lecture_name": lecture.lecture_name,
            "audience_id": lecture.audience_id,
            "group_id": lecture.group_id,
            "teacher_id": lecture.teacher_id,
            "lecture_day": lecture.lecture_day,
        } for lecture in lectures_query]
    return lectures


def get_lectures_for_group(student_id):
    lectures_query = Lectures.query.filter(Lectures.group_id == get_one_student(student_id)[0]["group_id"])
    lectures = [
        {
            "lecture_id": lecture.lecture_id,
            "lecture_name": lecture.lecture_name,
            "audience_id": lecture.audience_id,
            "group_id": lecture.group_id,
            "teacher_id": lecture.teacher_id,
            "lecture_day": lecture.lecture_day,
        } for lecture in lectures_query]
    return lectures


def get_one_audience(audience_id):
    audience_found = Audiences.query.filter(Audiences.audience_id == audience_id)
    result = [
        {
            "audience_id": audience.audience_id,
            "room_number": audience.room_number
        } for audience in audience_found]
    return result


def get_one_teacher(teacher_id):
    teacher_found = Teachers.query.filter(Teachers.teacher_id == teacher_id)
    result = [
        {
            "teacher_id": teacher.teacher_id,
            "teacher_name": teacher.teacher_name
        } for teacher in teacher_found]
    return result


def get_one_group(group_id):
    group_found = Groups.query.filter(Groups.group_id == group_id)
    result = [
        {
            "group_id": group.group_id,
            "group_name": group.group_name
        } for group in group_found]
    return result


def get_one_lecture(lecture_id):
    lecture_found = Lectures.query.filter(Lectures.lecture_id == lecture_id)
    result = [
        {
            "lecture_id": lecture.lecture_id,
            "lecture_name": lecture.lecture_name,
            "audience_id": lecture.audience_id,
            "group_id": lecture.group_id,
            "teacher_id": lecture.teacher_id,
            "lecture_day": lecture.lecture_day,
        } for lecture in lecture_found]
    return result
