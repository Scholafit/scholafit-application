from . import app_views
from app.controller.learning_module import add_user_subjects, create_user_exam, submit_exam, get_all_subjects
from flask import request

# create subjects
@app_views.route('/learner-center/subjects/<int:profile_id>', methods=['POST'])
def user_subjects(profile_id):
    return add_user_subjects(profile_id, request)

# generate tests
@app_views.route('/learner-center/tests/<int:profile_id>', methods=['POST'])
def get_test(profile_id):
    return create_user_exam(profile_id)

# submit the test
@app_views.route('/learner-center/tests/submit/<int:test_id>', methods=['POST'])
def submit_user_exam(test_id):
    return submit_exam(test_id, request)

# get all subjects
@app_views.route('/learner-center/subjects', methods=['GET'])
def get_available_subjects():
    
    return get_all_subjects()