from flask import make_response, jsonify, Request
from app.models.user import user

def create_user(request: Request):
    """
    Create a new user with the provided data.
    Args:
        data (dict): A dictionary containing user details (username, email, password).
    Returns:
        str: A success message or error message.
    """
    data = request.json
    email = data.get("email")
    try:
        existing_users = [u['email'] for u in user.get_all()]  
        
        if email in existing_users:
            return make_response(jsonify({"error": "Email already exists"}), 409)
        
        new_user = user.create_user(**data)
        return make_response(jsonify({"new_user": new_user}), 201)
    
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)


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
    #user.delete_user(user_id)
    try:
        deleted_user = user.delete_user(user_id)
        return make_response(jsonify({"deleted user": deleted_user}), 201)
    except Exception as e:
        return f"Error deleting user: {str(e)}"
    #return make_response(jsonify({"user": "user deleted successfully"}), 201)
