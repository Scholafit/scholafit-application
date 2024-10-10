from app.models.base_model import BaseModel
from app.models.database import Repository, get_db
from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey, Boolean, update, insert, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


DB = get_db()

class DB_Test(BaseModel):

    __tablename__ = "tests"

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey("profiles.id"), nullable=False)
    date_taken: Mapped[datetime] = mapped_column(default= lambda: datetime.now(timezone.utc), nullable=False)
    total_score: Mapped[int] = mapped_column(Integer, default=0)

    subject_tests: Mapped[List["DB_SubjectTest"]] = relationship(back_populates="test")

    def __init__(self, profile_id:int):
        self.profile_id = profile_id
        self.date_taken = datetime.now(timezone.utc)
        self.total_score = 0

class UserTestRepository(Repository):
    def __init__(self, database: SQLAlchemy):
        super().__init__(database)

    def get_test_questions_and_answers(self,test_id: int):
        test = self.database.session.execute(select(DB_Test).where(DB_Test.id==test_id)).scalar_one_or_none()
        
        if test:
            subjects = test.subject_tests
            return[db_test_question.question for subject in subjects for db_test_question in subject.test_questions ]
        


class UserTest:
    def __init__(self, repo: Repository):
        self.db = repo
    
    
    def create_test_record(self,profile_id: int):
        record = DB_Test(profile_id)
        return self.db.save(record).to_dict()
    
    def test_questions(self, test_id: int):
        test_question_objects = self.db.get_test_questions_and_answers(test_id)
        test_questions = []
        passages_in_test = []
        subjects = {}
        for test_question in test_question_objects:
            data = {}
            if test_question.passage and test_question.passage_id not in passages_in_test:
                passages_in_test.append(test_question.passage_id)
                passage_questions_all = test_question.passage.questions
                data["passage"] = test_question.passage.passage
                data["questions"] = [{"question": qn.question,"question_id":qn.id, "explanation": qn.answer_explanation,"answers": [{"text": a.answer_text, "answer_id": a.id,"is_correct": a.is_correct} for a in qn.answer_choices]} for qn in passage_questions_all]
            else:
                data["passage"] = None
                data["questions"] = [{"question": test_question.question, "question_id": test_question.id,"explanation": test_question.answer_explanation,"answers": [{"text": a.answer_text, "answer_id": a.id, "is_correct": a.is_correct} for a in test_question.answer_choices]}]
            

            subject_name = test_question.subject.name
            subject_id = test_question.subject_id
            if subject_name in subjects:
                subject_data = subjects[subject_name]
                subject_data["data"].append(data)
            else:
                subjects[subject_name] = {"subject_name": subject_name,"subject_id": subject_id, "data": [data]}
                test_questions.append(subjects[subject_name])
                
        
        return test_questions
        

    

    

class DB_SubjectTest(BaseModel):

    __tablename__ = "subject_tests"

    test_id: Mapped[int] = mapped_column(Integer, ForeignKey("tests.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(Integer, ForeignKey("subjects.id"), nullable=False)
    subject_score: Mapped[int] = mapped_column(Integer, default=0)

    test: Mapped["DB_Test"] = relationship(back_populates="subject_tests")
    test_questions: Mapped[List["DB_SubjectTestQuestion"]] = relationship(back_populates="subject_test")
    subject: Mapped["DB_Subject"] = relationship(back_populates="subject_tests")

    def __init__(self,test_id: int, subject_id: int):
        self.test_id = test_id
        self.subject_id = subject_id
        self.subject_score = 0


class SubjectTestRepository(Repository):
    def __init__(self, database:SQLAlchemy):
        super().__init__(database)

    
    def calculate_subject_score(self, test_id: int, answers: list[int]):
    
        subjects = self.database.session.execute(select(DB_SubjectTest).where(DB_SubjectTest.test_id == test_id)).scalars().all()
        results = []
        for sub in subjects:
            sub_results = {
                "subject_id": sub.subject_id,
                "subject_name": sub.subject.name,
                "score": 0
            }
            
            db_subject_test_questions = sub.test_questions
            for db_sub_question in db_subject_test_questions:
                question = db_sub_question.question
                for ans in question.answer_choices:
                    if ans.is_correct and ans.id in answers:
                        sub_results["score"] += 1
            
            results.append(sub_results)
        
        return results


class SubjectTest:
    def __init__(self, repo: Repository):
        self.db = repo
    
    def create_subject_test_record(self,test_id: int, subject_id: int):
        record = DB_SubjectTest(test_id, subject_id)
        return self.db.save(record).to_dict()


    def subject_test_evaluation(self, test_id: int, answers: list[int]):
        results = self.db.calculate_subject_score(test_id, answers)
        
        return results

class DB_SubjectTestQuestion(BaseModel):
    __tablename__ = "subject_test_questions"

    subject_test_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject_tests.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey("questions.id"), nullable=False)
    order: Mapped[int] = mapped_column(Integer, nullable=False)

    subject_test: Mapped["DB_SubjectTest"] = relationship(back_populates="test_questions")
    question: Mapped["DB_Question"] = relationship(back_populates="subject_tests")
    user_answer: Mapped["UserAnswer"] = relationship(back_populates="subject_test_question", uselist=False)

    def __init__(self, subject_test_id: int, question_id: int, question_number: int):
        self.subject_test_id = subject_test_id
        self.order = question_number
        self.question_id = question_id


class SubjectTestQuestionRepository(Repository):
    def __init__(self, database:SQLAlchemy):
        super().__init__(database)


class SubjectTestQuestion:
    def __init__(self, repo: Repository):
        self.db = repo

        
    def create_test_question_record(self,subject_test_id, question_id, question_number=1):
        record = DB_SubjectTestQuestion(subject_test_id, question_id, question_number)
        return self.db.save(record).to_dict()

class UserAnswer(BaseModel):
    __tablename__ = "user_subject_answers"

    subject_test_question_id: Mapped[int] = mapped_column(Integer, ForeignKey("subject_test_questions.id"), nullable=False)
    selected_question_choice: Mapped[int] = mapped_column(Integer, ForeignKey("question_choices.id"), nullable=False)
    subject_test_question: Mapped["DB_SubjectTestQuestion"] = relationship(back_populates="user_answer")

    @staticmethod
    def save_user_answer(subject_test_question_id: int, user_answer: id):
        DB.session.execute(insert(UserAnswer).values(
            subject_test_question_id=subject_test_question_id,
            selected_question_choice=user_answer
        ))
    
    




testRepo = UserTestRepository(DB)
subjectTestRepo = SubjectTestRepository(DB)
subjectQuestionRepo = SubjectTestQuestionRepository(DB)

userTest = UserTest(testRepo)
subjectTest = SubjectTest(subjectTestRepo)
subjectTestQuestion = SubjectTestQuestion(subjectQuestionRepo)