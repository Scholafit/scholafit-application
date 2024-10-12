from flask import make_response, jsonify, Request
from app.models.user import user
from sqlalchemy.exc import IntegrityError
import MySQLdb
from app.models.learning_module.subject import userSubject, subject
from app.models.learning_module.test import subjectTest,userTest
from app.models.learning_module.learning_service import generate_test_exam, create_user_test_record

import json

def create_user(request: Request):
    """
    Create a new user with the provided data.
    Args:
        data (dict): A dictionary containing user details (username, email, password).
    Returns:
        str: A success message or error message.
    """
    data = request.json
    try:
        new_user = user.create_user(**data)
        return make_response(jsonify({"new_user": new_user[0], "new_profile": new_user[1]}), 201)
    except IntegrityError as e:
        user.db.database.session.rollback()
        error_message = str(e.orig)
        if "Duplicate entry" in error_message:
            if "users.email" in error_message:
                return (jsonify({"error": "Email already exists"}), 409)
            elif "users.username" in error_message:
                return (jsonify({"error": "Username already exists"}), 409)
        return (jsonify({"error": "An error occurred during user creation"}), 500)

def create_profile(user_id:int, request: Request):
    
    data = request.json
    
    resp = user.create_user_profile(user_id, **data)
    return make_response(jsonify({"profile": resp}), 201)
    

def add_user_subjects(profile_id: int, request: Request):
    subjects = request.json
    subs = json.loads(subjects["subjects"])

    resp = userSubject.create_user_subjects(profile_id, subs)
    return make_response(jsonify({'subjects': resp}), 201)


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


def get_user():
    """
    Fetch all users from the database.
    Returns:
        list: A list of all users in dictionary format.
    """
    users = user.get_all()
    return make_response(jsonify({"all users": users}), 200)

def user_by_id(user_id):
    """Fetch a user by their id"""
    user_detail = user.get_user_by_id(user_id)

    if user_detail:
        return make_response(jsonify({"user": user_detail}), 200)
    
    else:
        return make_response(jsonify({"Error": 'user not found'}), 404)

def delete_user_by_id(user_id):
    """Delete a user by their id"""
    try:
        deleted_user = user.delete_user(user_id)
        return make_response(jsonify({"deleted user": deleted_user}), 201)
    except Exception as e:
        return make_response(jsonify(f"Error deleting user: {str(e)}"), 501)
