
from app.models.student import Student


def create(data):
    
    student = Student(**data)

    return student.create(student)


def get_students():
    return Student.students()
