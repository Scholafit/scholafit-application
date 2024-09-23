
from app.models.student import Student


def create(data):
    
    student = Student(**data)

    new_student = student.create_student()

    

    return new_student.to_dict()

def get_students():
    return Student.students()
