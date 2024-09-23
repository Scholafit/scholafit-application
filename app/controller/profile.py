from flask import make_response, jsonify, Request
from app.models.profile import profile



def create_user_profile(request: Request):
    data = request.json

    user_profile = profile.create_profile(**data)
    return make_response(jsonify({"profile": user_profile}), 200)

def get_user_profile(userId: int):

    
    user_profile = profile.get_profile_by_id(int(userId))

    if user_profile:
        return make_response(jsonify({"profile": user_profile, "msg": "SUCCESS"}), 200)
    
    return make_response(jsonify({"profile": None, "msg": 'profile not found'}), 404)