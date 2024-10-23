from flask import make_response, jsonify, Request
from app.models.user import user
from sqlalchemy.exc import IntegrityError
from app.utils.utils import create_session

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
        create_session(new_user[0]["id"])
        return make_response(jsonify({"new_user": new_user[0], "new_profile": new_user[1]}), 201)
    except IntegrityError as e:
        user.db.database.session.rollback()
        error_message = str(e.orig)
        if "Duplicate entry" in error_message:
            if "users.email" in error_message:
                return (jsonify({"status": "error", "code": "Email already exists", "status_code": 409,
                                 "errors": [{"field": "email", "error": "Email already exist"}]}), 409)
            elif "users.username" in error_message:
                return (jsonify({"status": "error", "code": "Username already exists", "status_code": 409,
                                 "errors": [{"field": "email", "error": "Username already exist"}]}), 409)
    except ValueError as e:
        error_message = str(e)
        if "Password" in error_message:
            return (jsonify({"status": "error", "code": "Password must be minimum 8 characters long, contain minimum 1 uppercase, minimum 1 lowercase and minimum 1 special character", "status_code": 409,
                             "errors": [{"field": "email", "error": "Password not strong enough"}]}), 409)
        return (jsonify({"status": "error", "code": "An error occurred during user creation", "status_code": 500,
                         "errors": [{"field": "email", "error": "An error occured during user creation"}]}), 500)

def create_profile(user_id:int, request: Request):
    
    data = request.json
    
    resp = user.create_user_profile(user_id, **data)
    return make_response(jsonify({"profile": resp}), 201)
    

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
