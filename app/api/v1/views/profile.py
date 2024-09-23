from . import app_views
from app.controller.profile import get_user_profile, create_user_profile
from flask import request

@app_views.route('/users/profile', methods=['POST'])
def create_profile():
    
    return create_user_profile(request)

@app_views.route('/users/<profileId>/profiles', methods=['GET'])
def get_profile(profileId):
   
    return get_user_profile(profileId)