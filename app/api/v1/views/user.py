from . import app_views
from app.controller.user import create_user, get_user, user_by_id, delete_user_by_id, create_profile, add_user_subjects, create_user_exam, submit_exam
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

# create a profile
@app_views.route('/users/profile/<int:user_id>', methods=['POST'])
def create_user_profile(user_id):
    return create_profile(user_id, request)


# create subjects
@app_views.route('/users/profile/subjects/<int:profile_id>', methods=['POST'])
def user_subjects(profile_id):
    return add_user_subjects(profile_id, request)

# generate tests
@app_views.route('/users/tests/<int:profile_id>', methods=['POST'])
def get_test(profile_id):
    return create_user_exam(profile_id)

# submit the test
@app_views.route('/users/tests/submit/<int:test_id>', methods=['POST'])
def submit_user_exam(test_id):
    print('submitting')
    return submit_exam(test_id, request)
