from flask import make_response, jsonify, Request, session
from app.models.learning_module.subject import userSubject, subject
from app.models.learning_module.test import subjectTest,userTest
from app.models.learning_module.learning_service import generate_test_exam, create_user_test_record, create_conversation_ai, chat_with_ai, create_user_profile
from datetime import datetime, timezone
from uuid import uuid4
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
    print(exam)
    return make_response(jsonify({"exam": exam, "test_id": test_id}), 200)

def submit_exam(test_id: int, request: Request):
    print('submitting exam')
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


def create_chat_with_ai(request: Request):
    session_id = session.get('session_id', None)
    if not session_id:
       return make_response(jsonify({
            "error": "Credentials provided are invalid",
            "status": "INVALID_CREDENTIALS",
            "status_code": 401,
            "errors": []
        }), 401)
    req = request.json
    prompt_message = req["message"]
    if prompt_message == '':
       return make_response(jsonify({
            "error": "prompt message cannot be an empty string",
            "status": "CLIENT_ERR",
            "status_code": 400,
            "errors": []
        }), 400)
    
    user_data = session.get(session_id)
    user_id = user_data["user_id"]
    conversations = user_data["conversations"]
    conversation_id = f"{uuid4()}-{user_id}"
    ai_response = create_conversation_ai(prompt_message.rstrip())
    
    updated_at = datetime.now(timezone.utc)
    conversations[conversation_id] = {

        "title": ai_response["title"],
        "subject": ai_response.get("subject", None),
        "updated_at": updated_at,
        "conversation": [{"user": prompt_message, "assistant": ai_response["response"]}]
    }

    session[session_id] = {
        "user_id": user_id,
        "conversations": conversations
    }
    ai_response["updated_at"] = updated_at
    return make_response(jsonify({"response":ai_response, "conversation_id": conversation_id}),201)


def continue_chat(conversation_id:str, request: Request):
    print(f'continue chat - {conversation_id}')
    session_id = session.get('session_id', None)
    req = request.json
    prompt_message = req["message"]
    user_data = session.get(session_id)
    conversations = user_data["conversations"]
    
    conversation = conversations[conversation_id]
    # print(conversation)
    if len(conversation) == 0:
        return make_response(jsonify({
            "error": "Invalid id",
            "status": "CLIENT_ERR",
            "status_code": 400,
            "errors": []
        }), 400)
    response = chat_with_ai(prompt_message, conversation["conversation"])

    updated_at = datetime.now(timezone.utc)
    conversation["updated_at"] = updated_at
    conversation["conversation"].append({
        "user": prompt_message,
        "assistant": response["response"]
    })
    conversations[conversation_id] = conversation
    session[session_id] = {
        "user_id": user_data["user_id"],
        "conversations": conversations
    }
    response["updated_at"] = updated_at
    return make_response(jsonify({"response": response, "conversation_id":conversation_id}), 200)

def get_chats():
    session_id = session.get('session_id', None)
    if not session_id:
        return make_response(jsonify({
            "error": "Credentials provided are invalid",
            "status": "INVALID_CREDENTIALS",
            "status_code": 401,
            "errors": []
        }), 401)
    user_data = session.get(session_id)
    conversations = user_data["conversations"]
    return make_response(jsonify({
        "chats": conversations
    }), 200)

def get_chat_by_id(conversation_id: str):
    session_id = session.get('session_id', None)
    if not session_id:
        return make_response(jsonify({
            "error": "Credentials provided are invalid",
            "status": "INVALID_CREDENTIALS",
            "status_code": 401,
            "errors": []
        }), 401)
    user_data = session.get(session_id)
    conversations = user_data["conversations"]
    conversation = conversations[conversation_id]
    if not conversation or len(conversation) == 0:
        return make_response(jsonify({
            "error": "Conversation not found",
            "status": "NOT_FOUND",
            "status_code": 404,
            "errors": []
        }), 404)
    return make_response(jsonify({
            "chat": conversation
        }), 200)


def initial_profile_build(profile_id, request: Request):
    req = request.json
    profile_data = req["profile_data"]
    subjects = req["subject_data"]
    
    response = create_user_profile(profile_data,subjects, profile_id)
    print(response)
    if not response:
        return make_response(jsonify({
            "status": "Failed to create profile",
            "code": "ERR",
            "status_code": 400,
            "errors": []
        }), 400)
    
    return make_response(jsonify({"response": "OK"}), 200)