from app.models.base_model import BaseModel
from app.models.database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
 

DB = get_db()


class DB_Subject(BaseModel):
    __tablename__ = "subjects"
    name:Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    isEnglish: Mapped[bool] = mapped_column(Boolean,nullable=False)
    questions: Mapped[List["DB_Question"]] = relationship(back_populates="subject", cascade="all, delete-orphan")
    subject_tests: Mapped["DB_SubjectTest"] = relationship(back_populates="subject")

    
    def __init__(self, name: str, isEnglish: bool):
        self.name = name.lower()
        self.isEnglish = isEnglish


class SubjectRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)

    def get_subject_by_name(self, name:str):
        
        return self.database.session.execute(select(DB_Subject).filter_by(name=name.lower())).scalar_one_or_none()
    
    def get_subject_by_id(self, subject_id: int):
        return self.database.session.execute(select(DB_Subject).where(DB_Subject.id==subject_id)).scalar_one_or_none()

class Subject:
    def __init__(self, subjectRepository: Repository):
        self.db = subjectRepository


    def create_subject(self, name: str, isEnglish: bool):
        subject = DB_Subject(name, isEnglish)
        return self.db.save(subject).to_dict()
    
    def get_subject_name(self, name: str):

        sub = self.db.get_subject_by_name(name.lower())
        return sub
    
    def get_subject_by_id(self, subject_id:int):
        return self.db.get_subject_by_id(subject_id)
    
    def get_subjects(self):
        return self.db.get_all(DB_Subject)






class DB_UserSubject(BaseModel):

    __tablename__ = "user_subjects"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)

    def __init__(self, profile_id, subject_id):
        self.profile_id = profile_id
        self.subject_id = subject_id


class UserSubjectRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)

    def add_subject(self,profile_id: int, subject_id: int):
        record = DB_UserSubject(profile_id, subject_id)
        return self.add(record)

    def get_user_subjects(self, profile_id: int):
        subs = self.database.session.execute(select(DB_UserSubject.subject_id).where(DB_UserSubject.profile_id == profile_id)).scalars().all()
        return subs
    
    def save_record(self):
        self.database.session.commit()

class UserSubject:
    def __init__(self, repo: Repository):
        self.db = repo
    
    def create_user_subjects(self, profile_id: int, subject_ids:list[int]):
        #check that user has a maximum of 4 subjects
        #check that each subject is unique
        #check that at least one of the subjects is English
        
        subjects = [self.db.add_subject(profile_id, sub).to_dict() for sub in subject_ids]

        self.db.save_record()

        return subjects
    
    def user_subjects(self, profile_id):
        return self.db.get_user_subjects(profile_id)
        



subRepo = UserSubjectRepository(DB)

userSubject = UserSubject(subRepo)


subject = Subject(SubjectRepository(DB))