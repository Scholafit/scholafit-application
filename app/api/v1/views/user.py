from . import app_views
from app.controller.user import create_user, get_user, user_by_id, delete_user_by_id
from flask import request

# Create a user
@app_views.route('/users', methods=['POST'])
def create_user_route():
    return create_user(request)

# Get a user by ID
@app_views.route('/users/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    return user_by_id(user_id)

# Delete a user
@app_views.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    return delete_user_by_id(user_id)

# Get all users
@app_views.route('/users', methods=['GET'])
def get_all_users_route():
    return get_user()
