from app.models.database import db

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "firt_name": self.firstname,
            "last_name": self.lastname,
            "email": self.email,
            "age": self.age,
        }

    def __init__(self, first_name, last_name, email, age):
        self.firstname = first_name
        self.lastname = last_name
        self.email = email
        self.age = age

    def create(self, student):
        db.session.add(student)
        db.session.commit()
        return 'created successfully'

    @classmethod
    def students(cls):
        students = db.session.execute(db.select(Student)).scalars()

        return [student.to_dict() for student in students]