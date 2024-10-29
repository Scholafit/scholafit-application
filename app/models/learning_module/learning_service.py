
from anthropic import Anthropic
from app.models.database import get_db
from app.models.error import AiModelError
from .ai import generate_questions, AI, create_anthropic_client
from .question import question, answerChoices, passage, DB_Question
from .subject import subject, userSubject
from app.models.profile import profile
from .test import userTest, subjectTest, subjectTestQuestion
from .user_question_history import DB_UserQuestionHistory
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload, joinedload
import json
import os
import re


## CONVERT THIS TO A CLASS
subjects = ['English', 'Mathematics', 'Physics', 'Accounting', 'Chemistry', 'Commerce', 'Animal Husbandry','Fishery', 'Agricultural Scienc', 'Economics', 'Geography', 'Further Mathematics', 'Literature in English', 'Goverment']

DB = get_db()

def create_subject(sub: str):
    is_english = True if sub.lower() == 'english' else False
    return subject.create_subject(sub, is_english) 

#generate question according to subject 
#get question and create passage if its english
#create question
#create answer choices

def extract_data_from_response(resp, match_pattern)-> list | None:
    if len(resp.content) == 0:
        raise AiModelError('The Ai model returned empty content')
    text_content = resp.content[0].text
    
    match = re.search(match_pattern, text_content, re.DOTALL)

    if match:
        json_string = match.group()
        cleaned_json_string = re.sub(r'\s+', ' ', json_string).strip()
        try:
            data = json.loads(cleaned_json_string)
            return data
        except json.JSONDecodeError as err:
            print(f'JSONDecodeError: {err}')
            print(f'Original json string: {json_string}')
            print(f'Cleaned JSON String: {cleaned_json_string}')
            raise err


def create_answers(answers: list, question_id: int):
    for answer in answers:
        is_correct_answer = answer.get("is_correct_answer")
        correct_answer = True if is_correct_answer or is_correct_answer == 'True' else False
        answerChoices.create_answer(answer.get("choice"), correct_answer, question_id)

def create_passage_based_question(data: dict, subject_id: int):
    explanation = data.get("explanation")
    questions = data.get("questions")
    passage_text = data.get("passage")
    psg = passage.create_passage(passage_text)
    passage_id = psg.get("id")
    for ques in questions:
        args = {

            "passage_id": passage_id,
            "question": ques.get("question"),
            "explanation": explanation,
            "subject_id": subject_id
        }
        quiz = question.create_question(**args)
        answers = ques.get("answers")
        create_answers(answers, quiz.get("id"))

def create_multiple_choice_question(data: dict, subject_id: int):
    explanation = data.get("explanation")
    questions = data.get("questions")
    for ques in questions:
        args = {
            "question": ques.get("question"),
            "explanation": explanation,
            "subject_id": subject_id
        }

        quiz = question.create_question(**args)
        answers = ques.get("answers")
        create_answers(answers, quiz.get("id"))


def get_questions_from_ai(subject_name: str, num_of_questions: int, client):
    response = generate_questions(subject_name, num_of_questions, client)
    data_regex_match_pattern = r'\[.*\]'
    data = extract_data_from_response(response, data_regex_match_pattern)
    return data


def add_question_to_storage(subject_id: int, data):
   
    for dt in data:
        question_type:str = dt.get("type")

        if question_type.lower() == "passage_based":
            create_passage_based_question(dt, subject_id)
        else:
            create_multiple_choice_question(dt, subject_id)



NEW_QUESTION_LIMIT = 60
SEEN_QUESTION_LIMIT = 40
TOTAL_QUESTIONS = 20
def create_test(profile_id: int, subject_ids: list[int]) -> list[DB_Question]:
    print('creating test')
    print(f'subject_ids---- {subject_ids}')
  
    new_questions_limit = int((NEW_QUESTION_LIMIT / 100) * TOTAL_QUESTIONS)
    seen_questions_limit = TOTAL_QUESTIONS - new_questions_limit

    user_history_exists = DB.session.execute(
        select(DB_UserQuestionHistory).filter_by(profile_id=profile_id)).first()
    print(f'user_history_exists {user_history_exists}')
    if not user_history_exists:
        new_questions_limit = TOTAL_QUESTIONS

    print(new_questions_limit)
    new_question_query = (
        select(DB_Question.id)
        .outerjoin(DB_UserQuestionHistory, 
                  and_(DB_UserQuestionHistory.question_id == DB_Question.id,
                       DB_UserQuestionHistory.profile_id == profile_id))
        .where(DB_UserQuestionHistory.question_id.is_(None))
        .where(DB_Question.subject_id.in_(subject_ids))
        .order_by(func.random())
        .limit(new_questions_limit)
    )

    seen_question_query = (
        select(DB_Question.id)
        .join(DB_UserQuestionHistory, 
                  and_(DB_UserQuestionHistory.question_id == DB_Question.id,
                       DB_UserQuestionHistory.profile_id == profile_id))
        .where(DB_Question.subject_id.in_(subject_ids))
        .order_by(func.random())
        .limit(seen_questions_limit)
    )

    combined_query = new_question_query.union_all(seen_question_query)
    question_ids = DB.session.execute(combined_query).scalars().all()
    print(f'question_ids--- {question_ids}')
    test_question_query = (
        select(DB_Question)
        .where(DB_Question.id.in_(question_ids))
        .options(
            selectinload(DB_Question.passage),
            selectinload(DB_Question.answer_choices)
        )
    )
    test_question_objects = DB.session.execute(test_question_query).scalars().all()

    return test_question_objects


def generate_test_exam(profile_id: int, subject_ids: list[int]):

    print('generating test')
    test_question_objects = create_test(profile_id, subject_ids)
    print(f'test object list {test_question_objects}')
    test_questions = []
    passages_in_test = []
    subjects = {}
    for test_question in test_question_objects:
        print('generating test')
        print(f'subjects dict-- {subjects}')
        data = {}
        if test_question.passage and test_question.passage_id not in passages_in_test:
            passages_in_test.append(test_question.passage_id)
            passage_questions_all = test_question.passage.questions
            data["passage"] = test_question.passage.passage
            data["questions"] = [{"question": qn.question,"question_id":qn.id, "answers": [{"text": a.answer_text, "answer_id": a.id, "correct": a.is_correct} for a in qn.answer_choices]} for qn in passage_questions_all]
        else:
            data["passage"] = None
            data["questions"] = [{"question": test_question.question, "question_id": test_question.id,"answers": [{"text": a.answer_text, "answer_id": a.id, "correct": a.is_correct} for a in test_question.answer_choices]}]
        
        subject_name = test_question.subject.name
        subject_id = test_question.subject_id
        print(f'subject name {subject_name}')
        if subject_name in subjects:
            subject_data = subjects[subject_name]
            subject_data["data"].append(data)
        else:
            subjects[subject_name] = {"subject_name": subject_name,"subject_id": subject_id, "data": [data]}
            test_questions.append(subjects[subject_name])
        print(f'data is --{data}')   
    
    return test_questions


def create_user_test_record(profile_id, exam:list[dict[str, any]]):
    u_test = userTest.create_test_record(profile_id)
    
    test_id = u_test["id"]
    
    for ex in exam:
        sub_id = ex["subject_id"]
    
        exam_data = ex["data"]
        sub_test = subjectTest.create_subject_test_record(test_id, sub_id)
        sub_test_id = sub_test["id"]
        
        for ex_dt in exam_data:
            questions = ex_dt["questions"]
            for question in questions:
                question_id = question["question_id"]
                d = subjectTestQuestion.create_test_question_record(sub_test_id,question_id)

    return test_id


 
anthropic_client = create_anthropic_client()
ai_bot = AI(anthropic_client)    

def create_conversation_ai(prompt_message:str):
    try:

        response = ai_bot.ai_chat(prompt_message)
        data_regex_match_pattern = r'\{[\s\S]*\}'
        data = extract_data_from_response(response, data_regex_match_pattern)
        return data
    except AiModelError as e:
        return str(e)
    except Exception as e:
        print(e)
        
def chat_with_ai(prompt_message: str, chat_history: list):
   
    try:
        response = ai_bot.continue_chat_ai(prompt_message, chat_history)
        data_regex_match_pattern = r'\{[\s\S]*\}'
        data = extract_data_from_response(response, data_regex_match_pattern)
        return data
    except AiModelError as e:
        return str(e)
    except Exception as e:
        print(e)


def create_user_profile(profile_data, subjects_data, profile_id):
    user_profile = profile.update_profile(profile_id, **profile_data)
    if user_profile:
        user_selection = [subject.get_subject_name(sb) for sb in subjects_data]
        print(f'user-select {user_selection}')
        subject_ids = [sub["id"] for sub in user_selection]
        print(f'subject_ids --{subject_ids}')
        user_subjects = userSubject.create_user_subjects(profile_id, subject_ids)
        print(f'user_subject list{user_subjects}')
        # fix error here sb.to_dict not a function
        user_subjects = [sb.to_dict() for sb in user_subjects]
        return {
            "profile": user_profile,
            "subjects": user_subjects
        }

    return None