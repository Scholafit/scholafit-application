from app.models.base_model import BaseModel
from sqlalchemy import Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List



class Question(BaseModel):

    __tablename__ = "questions"

    content: Mapped[str] = mapped_column(Text, nullable=False)
    answer_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    is_pregenerated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)

    subject: Mapped["Subject"] = relationship(back_populates="questions")
    answer_choices:Mapped[List["QuestionAnswerChoices"]] = relationship(back_populates="question", cascade="all, delete-orphan")




class QuestionAnswerChoices(BaseModel):

    __tablename__ = "question_choices"

    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False)
    question: Mapped["Question"] = relationship(back_populates="answer_choices")