
from app.models.base_model import BaseModel
from app.models.database import Repository, get_db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Text, ForeignKey, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


DB = get_db()

class DB_Question(BaseModel):

    __tablename__ = "questions"

    question: Mapped[str] = mapped_column(Text, nullable=False)
    answer_explanation: Mapped[str] = mapped_column(Text, nullable=False)
    is_pregenerated: Mapped[bool] = mapped_column(Boolean, nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)
    passage_id: Mapped[int] = mapped_column(Integer, ForeignKey("passages.id"), nullable=True)

    passage: Mapped["DB_Passage"] = relationship(back_populates="questions")
    subject: Mapped["DB_Subject"] = relationship(back_populates="questions")
    answer_choices:Mapped[List["DB_QuestionAnswerChoices"]] = relationship(back_populates="question", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        self.passage_id = kwargs.get('passage_id', None)
        self.question = kwargs.get("question")
        self.answer_explanation = kwargs.get("explanation")
        self.is_pregenerated = True
        self.subject_id = kwargs.get("subject_id")


class QuestionRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)


class Question:
    def __init__(self, questionRepository: Repository):
        self.db = questionRepository


    def create_question(self, **kwargs):
        question = DB_Question(**kwargs)
        return self.db.save(question).to_dict()


class DB_QuestionAnswerChoices(BaseModel):

    __tablename__ = "question_choices"

    answer_text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False)
    question: Mapped["DB_Question"] = relationship(back_populates="answer_choices")

    def __init__(self, answer, is_correct, question_id):
        self.answer_text = answer
        self.is_correct = is_correct
        self.question_id = question_id


class QuestionAnswerRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)


class QuestionAnswer:
    def __init__(self, questionAnswerRepository: Repository):
        self.db = questionAnswerRepository


    def create_answer(self, answer, is_correct, question_id):
        
        ans = DB_QuestionAnswerChoices(answer, is_correct, question_id)
        return self.db.save(ans).to_dict()


class DB_Passage(BaseModel):
    __tablename__ = "passages"

    passage: Mapped[str] = mapped_column(Text, nullable=True)
    questions: Mapped[List["DB_Question"]] = relationship(back_populates="passage")

    def __init__(self, passage):
        self.passage = passage

class PassageRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)


class Passage:
    def __init__(self, repository: Repository) -> None:
        self.db = repository
    

    def create_passage(self, passage_text):
        psg = DB_Passage(passage_text)
        return self.db.save(psg).to_dict()
    


question = Question(QuestionRepository(DB))

answerChoices = QuestionAnswer(QuestionAnswerRepository(DB))

passage = Passage(PassageRepository(DB))

