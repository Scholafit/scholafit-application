from . import app_views
from app.controller.learning_module import add_user_subjects, create_user_exam, submit_exam, get_all_subjects, create_chat_with_ai, continue_chat, get_chats,get_chat_by_id,initial_profile_build
from flask import request

# create subjects
@app_views.route('/learner-center/subjects/<int:profile_id>', methods=['POST'])
def user_subjects(profile_id):
    return add_user_subjects(profile_id, request)

@app_views.route('/learner-center/learner-profile/<int:profile_id>', methods=['POST'])
def initialize_profile(profile_id):
    print('In route')
    return initial_profile_build(profile_id, request)


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


#get previous chats
@app_views.route('/learner-center/ai', methods=['GET'])
def fetch_chats():
    return get_chats()

#get chat by id

@app_views.route('/learner-center/ai/<string:conversation_id>', methods=['GET'])
def fetch_chat_by_id(conversation_id):
    return get_chat_by_id(conversation_id)


# start conversation with AI
@app_views.route('/learner-center/ai', methods=['POST'])
def start_chat():
    return create_chat_with_ai(request)

# continue conversation with AI
@app_views.route('/learner-center/ai/<string:conversation_id>', methods=['POST'])
def continue_chat_with_ai(conversation_id):
    print('in api endpoint calling controller')
    return continue_chat(conversation_id, request)