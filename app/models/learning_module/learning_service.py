
from anthropic import Anthropic
from .ai import generate_questions
from .question import question, answerChoices, passage
from .subject import subject
import json
import os
import re



subjects = ['English', 'Mathematics', 'Physics', 'Accounting', 'Chemistry', 'Commerce', 'Animal Husbandry','Fishery', 'Agricultural Scienc', 'Economics', 'Geography', 'Further Mathematics', 'Literature in English', 'Goverment']



def create_subject(sub: str):
    is_english = True if sub.lower() == 'english' else False
    return subject.create_subject(sub, is_english) 

#generate question according to subject 
#get question and create passage if its english
#create question
#create answer choices

def extract_data_from_response(resp)-> list | None:
    text_content = resp.content[0].text
    pattern = r'\[.*\]'
    match = re.search(pattern, text_content, re.DOTALL)

    if match:
        json_string = match.group()
        try:
            data = json.loads(json_string)
            return data
        except json.JSONDecodeError as err:
            raise err


def create_answers(answers: list, question_id: int):
    for answer in answers:
        correct_answer = True if answer.get("is_correct_answer") == "True" else False
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
    data = extract_data_from_response(response)
    return data


def add_question_to_storage(subject_id: int, data):
   
    for dt in data:
        question_type:str = dt.get("type")

        if question_type.lower() == "passage_based":
            create_passage_based_question(dt, subject_id)
        else:
            create_multiple_choice_question(dt, subject_id)

    