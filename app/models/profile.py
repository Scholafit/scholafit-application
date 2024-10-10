from .base_model import BaseModel
from .database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, JSON, Integer, ForeignKey
from sqlalchemy.dialects.mysql import ENUM
from sqlalchemy.orm import Mapped, mapped_column, relationship


class DB_Profile(BaseModel):

    __tablename__ = 'profiles'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    subscription_status: Mapped[ENUM] = mapped_column(ENUM('ACTIVE', 'INACTIVE'), nullable=True)
    isAdult: Mapped[bool] = mapped_column(nullable=True)
    current_education_level: Mapped[str] = mapped_column(String(120), nullable=True)
    school_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    expected_graduation_year: Mapped[str | None] = mapped_column(String(4), nullable=True)
    desired_course: Mapped[str | None] = mapped_column(String(120), nullable=True)   
    university_choices: Mapped[list[str] | None] = mapped_column(JSON, nullable=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True)
    state: Mapped[str | None] = mapped_column(String(120), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(60), nullable=True)
    city: Mapped[str | None] = mapped_column(String(120), nullable=True)
    parent_first_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    parent_last_name: Mapped[str | None] = mapped_column(String(120), nullable=True)
    parent_email: Mapped[str | None] = mapped_column(String(120), nullable=True)
    parent_phone_number: Mapped[str | None] = mapped_column(String(15), nullable=True)

    user = relationship("DB_User", back_populates="profile")

    def __init__(self,**kwargs):

        self.user_id = kwargs.get('user_id')
        self.subscription_status = kwargs.get('subscription_status')
        self.current_education_level = kwargs.get('current_education_level')
        self.isAdult = True if kwargs.get('isAdult') == 'TRUE' else False


class ProfileRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)

    

class Profile:
    def __init__(self, dbRepository: Repository) -> None:

        self.db = dbRepository

    def create_profile(self, user_id, **kwargs):
        profile = DB_Profile(user_id=user_id, **kwargs)
        saved_profile = self.db.save(profile)
        return saved_profile.to_dict()
    
    def get_all(self):
        profile = self.db.get_all(DB_Profile)
        return [user_profile.to_dict() for user_profile in profile]
    
    def get_profile_by_id(self, profile_id:int) -> DB_Profile | None:
        profile = self.db.get_by_id(DB_Profile, profile_id)
        if profile:
            return profile.to_dict()
        else:
            return None
        
    def update_profile(self, profile_id: int, **kwargs) -> dict | None:
        profile = self.db.database.session.query(DB_Profile).filter_by(id=profile_id).first()
        if not profile:
            return None
    
        for key, value in kwargs.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
    
        self.db.database.session.commit()
        updated_profile = self.db.get_by_id(DB_Profile, profile_id)
        return updated_profile.to_dict()


database = get_db()

profileRepo = ProfileRepository(database)

profile = Profile(profileRepo)