from app.models.base_model import BaseModel
from app.models.database import Repository
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
 

class DB_Subject(BaseModel):
    __tablename__ = "subjects"
    name:Mapped[str] = mapped_column(String(120), nullable=False)
    isEnglish: Mapped[bool] = mapped_column(Boolean, nullable=False)
    questions: Mapped[List["DB_Question"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

    def __init__(self, name: str, isEnglish: bool):
        self.name = name
        self.isEnglish = isEnglish


class SubjectRepository(Repository):
     def __init__(self, database: SQLAlchemy):
        super().__init__(database)



class Subject:
    def __init__(self, subjectRepository: Repository):
        self.db = subjectRepository


    def create_subject(self, name: str, isEnglish: bool):
        subject = DB_Subject(name, isEnglish)
        return self.db.save(subject).to_dict()






class UserSubject(BaseModel):

    __tablename__ = "user_subjects"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)