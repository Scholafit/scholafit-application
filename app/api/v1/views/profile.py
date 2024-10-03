from . import app_views
from app.controller.profile import get_user_profile, create_user_profile, get_profiles, update_user_profile
from flask import request

@app_views.route('/users/profiles', methods=['GET'])
def get_all_profile():
    
    return get_profiles()

@app_views.route('/users/<profileId>/profiles', methods=['GET'])
def get_profile(profileId):
   
    return get_user_profile(profileId)

@app_views.route('/users/<profileId>/profiles', methods=['PUT'])
def update_profile(profileId):

    return update_user_profile(profileId)