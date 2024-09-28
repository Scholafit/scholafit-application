from app.models.base_model import BaseModel
from datetime import datetime, timezone
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column


class Test(BaseModel):

    __tablename__ = "tests"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    date_taken: Mapped[datetime] = mapped_column(default= lambda: datetime.now(timezone.utc), nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, default=0)


class SubjectTest(BaseModel):

    __tablename__ = "subject_tests"

    test_id: Mapped[int] = mapped_column(Integer, ForeignKey("tests.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)
    subject_score: Mapped[int] = mapped_column(Integer, default=0)


class SubjectTestQuestion(BaseModel):
    __tablename__ = "subject_test_questions"

    subject_test_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject_tests.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)


class UserAnswer(BaseModel):
    __tablename__ = "user_subject_answers"

    subject_test_question_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject_test_questions.id"), nullable=False)
    selected_question_choice: Mapped[int] = mapped_column(Integer, ForeignKey("question_choices.id"), nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)