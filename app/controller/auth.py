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
