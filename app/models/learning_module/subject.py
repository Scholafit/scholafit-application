from app.models.base_model import BaseModel
from sqlalchemy import String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
 

class Subject(BaseModel):
    __tablename__ = "subjects"
    name:Mapped[str] = mapped_column(String(120), nullable=False)
    isEnglish: Mapped[bool] = mapped_column(Boolean, nullable=False)
    questions: Mapped[List["Question"]] = relationship(back_populates="subject", cascade="all, delete-orphan")


class UserSubject(BaseModel):

    __tablename__ = "user_subjects"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)