from .base_model import BaseModel
from .database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..services.secure_pass import hash_password
from ..services.notification import create_email_notification_service
from .profile import DB_Profile, Profile
from itsdangerous import URLSafeTimedSerializer
import os

class DB_User(BaseModel):

    __tablename__ = 'users'

    first_name: Mapped[str] = mapped_column(String(120), nullable=False)
    last_name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    #profile_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Link to profile data if necessary
    roles: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)    # Roles like 'admin', 'user', etc.

    profile = relationship("DB_Profile", back_populates="user", uselist=False)
    subscription = relationship("DB_Subscription", back_populates="user", uselist=False)

    def __init__(self, **kwargs):

        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        plain_password = kwargs.get('password')
        self.password = hash_password(plain_password)
        self.is_active = kwargs.get('is_active', True)
        self.is_verified = kwargs.get('is_verified', False)
        self.profile_data = kwargs.get('profile_data')
        self.roles = kwargs.get('roles', ['user'])

    def to_dict(self):
        user_dict = super().to_dict()
        if self.profile:
            user_dict["profile_data"] = self.profile.to_dict()
        return user_dict

class UserRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)
    # Define custom queries here if needed


class User:
    def __init__(self, dbRepository: Repository) -> None:
        self.db = dbRepository
        self.serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))

    def create_user(self, **kwargs):
        required_fields = ['first_name', 'last_name', 'username', 'email', 'password']
        for field in required_fields:
            if field not in kwargs or not kwargs[field]:
                raise ValueError(f"Missing required field: {field}")

        user = DB_User(**kwargs)
        saved_user = self.db.save(user)

        blank_profile_data = {
            "user_id": saved_user.id,
            "subscription_status": 'INACTIVE',
            "isAdult": False,
            "current_education_level": "JSS",
            "school_name": None,
            "expected_graduation_year": None,
            "desired_course": None,
            "university_choices": [],
            "country": None,
            "state": None,
            "postal_code": None,
            "city": None,
            "parent_first_name": None,
            "parent_last_name": None,
            "parent_email": None,
            "parent_phone_number": None
        }
        blank_profile = DB_Profile(**blank_profile_data)
        new_profile = self.db.save(blank_profile)


        token = self.serializer.dumps(saved_user.email, salt='verify-email-salt')

        #Send verification link to the new user
        subject = f"Congratulations {saved_user.first_name} You are on your way to acing your upcoming examinations"
        verify_link = f"127.0.0.1:5000/api/v1/verify/{token}"
        message = f"Please click the following link to verify your user account\n {verify_link}"
        sender_address = "info@scholafit.com"
        email_service = create_email_notification_service(sender_address)
        email_service.notify(saved_user.email, message, subject)
        dict_user = saved_user.to_dict()
        return dict_user, new_profile.to_dict()
    
    
    def get_all(self):
        users = self.db.get_all(DB_User)
        return [person.to_dict() for person in users]
    
    def get_user_by_id(self, user_id:int) -> DB_User | None:
        user = self.db.get_by_id(DB_User, user_id)
        if user:
            return user.to_dict()
        return None
    
    def delete_user(self, user_id: int):
        user = self.db.get_by_id(DB_User, user_id)
        if user:
            if user.profile:
                self.db.delete(user.profile)
            if user.subscription:
                self.db.delete(user.subscription)

            self.db.delete(user)
            return {"deleted": user.to_dict()}
        return "User not found"

# Initialize database and repository
database = get_db()
userRepo = UserRepository(database)
user = User(userRepo)