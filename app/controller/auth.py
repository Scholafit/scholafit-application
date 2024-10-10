from flask import make_response, jsonify, Request
from app.models.auth import auth_service

def login(request: Request):
    """
    Authenticate user with email and password.
    Args:
        request (Request): Request containing user credentials.
    Returns:
        JSON: A success message or error message.
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')

    try:
        login_response = auth_service.login(email, password)
        if "error" in login_response:
            return make_response(jsonify(login_response), 401)
        return make_response(jsonify(login_response), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)


def logout():
    """Logout the authenticated user."""
    try:
        logout_response = auth_service.logout()
        return make_response(jsonify(logout_response), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)

def forgot_password(request: Request):
    """
    Handle forgot password request.
    Args:
        request (Request): Request containing user email.
    Returns:
        JSON: A success message or error message.
    """
    data = request.json
    email = data.get('email')

    try:
        forgot_response = auth_service.forgot_password(email)
        if "error" in forgot_response:
            return make_response(jsonify(forgot_response), 404)
        return make_response(jsonify(forgot_response), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)


def reset_password(request: Request, token: str):
    """
    Handle password reset request.
    Args:
        request (Request): Request containing new password.
        token (str): The password reset token.
    Returns:
        JSON: A success message or error message.
    """
    data = request.json
    new_password = data.get('new_password')

    try:
        reset_response = auth_service.reset_password(token, new_password)
        if "error" in reset_response:
            return make_response(jsonify(reset_response), 400)
        return make_response(jsonify(reset_response), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)
    
def verify_new_user(request: Request, token: str):
    """
    Handle verification of a user email address
    Args:
        request (Request): Request containing new password.
        token (str): verification token.
    Returns:
        JSON: A success message or error message.
    """
    try:
        response = auth_service.verify_user(token)
        if 'error' in response:
            return make_response(jsonify(response), 400)
        return make_response(jsonify(response), 200)
    except Exception as e:
        return make_response(jsonify({"error": f"An error occurred: {str(e)}"}), 500)