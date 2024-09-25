from .base_model import BaseModel
from .database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..services.secure_pass import hash_password
from .profile import DB_Profile

class DB_User(BaseModel):

    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(120), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    profile_data: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # Link to profile data if necessary
    roles: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)    # Roles like 'admin', 'user', etc.

    profile = relationship("DB_Profile", back_populates="user", uselist=False)

    def __init__(self, **kwargs):
        self.username = kwargs.get('username')
        self.email = kwargs.get('email')
        plain_password = kwargs.get('password')
        self.password = hash_password(plain_password)
        self.is_active = kwargs.get('is_active', True)
        self.is_verified = kwargs.get('is_verified', False)
        self.profile_data = kwargs.get('profile_data')
        self.roles = kwargs.get('roles', ['user'])

class UserRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)
    # Define custom queries here if needed


class User:
    def __init__(self, dbRepository: Repository) -> None:
        self.db = dbRepository

    def create_user(self, **kwargs):
        user = DB_User(**kwargs)
        saved_user = self.db.save(user)
        return saved_user.to_dict()
    
    
    def create_user_profile(self, user_id: int, **profile_data):
        user = self.db.get_by_id(DB_User, user_id)
        if not user:
            return {"error": "User not found"}

        if user.profile:  # Ensure a profile does not already exist for the user
            return {"error": "Profile already exists for this user"}

        profile = DB_Profile(user_id=user_id, **profile_data)
        saved_profile = self.db.save(profile)
        return saved_profile.to_dict()
    
    def get_all(self):
        users = self.db.get_all(DB_User)
        return [person.to_dict() for person in users]
    
    def get_user_by_id(self, user_id:int) -> DB_User | None:
        user = self.db.get_by_id(DB_User, user_id)
        if user:
            return user.to_dict()
        return "id does not match any user"
    
    def delete_user(self, user_id: int):
        user = self.db.get_by_id(DB_User, user_id)
        if user:
            if user.profile:
                self.db.delete(user.profile)
            self.db.delete(user)
            return {"deleted": user.to_dict()}
        return "User not found"

# Initialize database and repository
database = get_db()
userRepo = UserRepository(database)
user = User(userRepo)