from app.models.base_model import BaseModel
from app.models.database import Repository
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, DateTime, select
from sqlalchemy.orm import Mapped, mapped_column


class DB_UserQuestionHistory(BaseModel):

    __tablename__ = "user_questions_history"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id'), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey('questions.id'), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime,nullable=False)
    times_seen: Mapped[int] = mapped_column(Integer, nullable=False)

    def __init__(self, **kwargs):

        self.user_id = kwargs.get("profile_id")
        self.question_id = kwargs.get("question_id")
        self.last_seen = datetime.now(timezone.utc)
        self.times_seen = 1

class UserQuestionHistoryRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)
    

    def create_record(self, **kwargs):
        question_id = kwargs.get("question_id")
        profile_id = kwargs.get("profile_id")

        database = self.database
        stmt = select(DB_UserQuestionHistory).where(
            DB_UserQuestionHistory.profile_id == profile_id,
            DB_UserQuestionHistory.question_id == question_id
        )
        record = database.session.execute(stmt).scalar_one_or_none()
        if record:
            record.times_seen += 1
            record.last_seen = datetime.now(timezone.utc)
            database.session.commit()
            database.session.refresh(record)
            return record.to_dict()
        
        new_record = DB_UserQuestionHistory(**kwargs)
        return self.save(new_record).to_dict()
        

class UserQuestionHistory:
    def __init__(self, historyRepository: Repository):
        self.db = historyRepository


    def create_user_question_history(self, **kwargs):
        record = self.db.create_record(**kwargs)
        return record
        
        
        

    