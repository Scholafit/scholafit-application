from app.models.base_model import BaseModel
from app.models.database import Repository, get_db
from app.models.error import ValidationError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, select, func
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
    """
    A repository class for managing subjects in the database.
    
    Inherits from the Repository class and provides methods to 
    query subjects by name or ID.
    """
    def __init__(self, database: SQLAlchemy):
        """
        Initializes the SubjectRepository with a database connection.

        Args:
            database (SQLAlchemy): An instance of SQLAlchemy for database operations.
        """
        super().__init__(database)

    def get_subject_by_name(self, name: str):
        """
        Retrieves a subject from the database by its name.

        Args:
            name (str): The name of the subject to search for (case-insensitive).

        Returns:
            DB_Subject or None: The subject object if found, otherwise None.
        """
        return self.database.session.execute(select(DB_Subject).where(func.lower( DB_Subject.name)==func.lower(name))).scalar_one_or_none()
    
    def get_subject_by_id(self, subject_id: int):
        """
        Retrieves a subject from the database by its ID.

        Args:
            subject_id (int): The ID of the subject to search for.

        Returns:
            DB_Subject or None: The subject object if found, otherwise None.
        """
        return self.database.session.execute(select(DB_Subject).where(DB_Subject.id == subject_id)).scalar_one_or_none()

class Subject:
    """
    A class to manage subject-related operations.
    
    Interacts with the SubjectRepository to create, retrieve,
    and manipulate subject data.
    """
    def __init__(self, subjectRepository: Repository):
        """
        Initializes the Subject class with a SubjectRepository instance.

        Args:
            subjectRepository (Repository): An instance of SubjectRepository to interact with the database.
        """
        self.db = subjectRepository

    def create_subject(self, name: str, isEnglish: bool):
        """
        Creates a new subject and saves it to the database.

        Args:
            name (str): The name of the subject.
            isEnglish (bool): Indicates whether the subject is English or not.

        Returns:
            dict: A dictionary representation of the created subject.
        """
        subject = DB_Subject(name, isEnglish)
        return self.db.save(subject).to_dict()
    
    def get_subject_name(self, name: str):
        """
        Retrieves a subject by its name.

        Args:
            name (str): The name of the subject to search for (case-insensitive).

        Returns:
            DB_Subject or None: The subject object if found, otherwise None.
        """
        sub = self.db.get_subject_by_name(name.lower())
        if sub:
            return sub.to_dict()
    
    def get_subject_by_id(self, subject_id: int):
        """
        Retrieves a subject by its ID.

        Args:
            subject_id (int): The ID of the subject to search for.

        Returns:
            DB_Subject or None: The subject object if found, otherwise None.
        """
        sub = self.db.get_subject_by_id(subject_id)
        if sub:
            return sub.to_dict()
    
    def get_subjects(self):
        """
        Retrieves all subjects from the database.

        Returns:
            list: A list of dictionaries representing all subjects.
        """

        # raise an exception if subjects is an empty list  - add later
        subjects = [subject.to_dict() for subject in self.db.get_all(DB_Subject)]
        return subjects




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

    MAX_SELECTABLE_SUBJECTS = 4
    def __init__(self, repo: Repository):
        self.db = repo
    
    def create_user_subjects(self, profile_id: int, subject_ids:list[int]):
        #check that user has a maximum of 4 subjects
        #check that each subject is unique
        #check that at least one of the subjects is English
        if len(subject_ids) > self.MAX_SELECTABLE_SUBJECTS:
            raise ValidationError("Selected more than the required number of subjects")
        current_subjects = self.user_subjects(profile_id)
        
        subjects = [self.db.add_subject(profile_id, sub).to_dict() for sub in subject_ids]

        self.db.save()

        return subjects
    
    def user_subjects(self, profile_id):
        return self.db.get_user_subjects(profile_id)
        



subRepo = UserSubjectRepository(DB)

userSubject = UserSubject(subRepo)


subject = Subject(SubjectRepository(DB))