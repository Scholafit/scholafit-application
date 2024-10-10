from app.services.notification import get_email_notification_service
from .database import db
from .base_model import BaseModel

class Student(BaseModel):
    
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def __init__(self, first_name, last_name, email, age):
        super().__init__()
        self.firstname = first_name
        self.lastname = last_name
        self.email = email
        self.age = age

    def create_student(self):
        student = self.create()
        return student

    @classmethod
    def students(cls):
        
        students = db.session.execute(db.select(Student)).scalars()

        return [student.to_dict() for student in students]