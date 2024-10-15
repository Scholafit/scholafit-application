from flask import make_response, jsonify, Request
from app.models.learning_module.subject import userSubject, subject
from app.models.learning_module.test import subjectTest,userTest
from app.models.learning_module.learning_service import generate_test_exam, create_user_test_record
import json

def add_user_subjects(profile_id: int, request: Request):
    subjects = request.json
    subs = json.loads(subjects["subjects"])

    resp = userSubject.create_user_subjects(profile_id, subs)

    data = []
    for res in resp:
        sub_id = res.get("subject_id")
        sub = subject.get_subject_by_id(sub_id)
        data.append(sub.name)
    return make_response(jsonify({'subjects': data}), 201)


def create_user_exam(profile_id:int):
    subs = userSubject.user_subjects(profile_id)
    exam = generate_test_exam(profile_id, subs)
    test_id = create_user_test_record(profile_id, exam)
    
    return make_response(jsonify({"exam": exam, "test_id": test_id}), 200)

def submit_exam(test_id: int, request: Request):
    req = request.json
    answer_ids = json.loads(req["answers"])
    results = subjectTest.subject_test_evaluation(test_id, answer_ids)
    questions = userTest.test_questions(test_id)
    
    for question in questions:
        data= question.get("data")
        for dt in data:
            question_b = dt.get("questions")
            for qz in question_b:
                answers=qz.get("answers")
                qz["user_answer_id"] = None
                for answer in answers:
                    if answer.get("answer_id") in answer_ids:
                        qz["user_answer_id"] = answer.get("answer_id")

 
    return make_response(jsonify({"results": results, "questions": questions}), 200)



def get_all_subjects():
    subjects = subject.get_subjects()

    return make_response(jsonify({"subjects": subjects}), 200)