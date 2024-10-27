from flask import make_response, jsonify, Request, request
from app.models.profile import profile



def create_user_profile(request: Request):
    data = request.json

    user_profile = profile.create_profile(**data)
    return make_response(jsonify({"profile": user_profile}), 200)

def get_profiles():
    """
    Fetch all users from the database.
    Returns:
        list: A list of all users in dictionary format.
    """
    profiles = profile.get_all()
    return make_response(jsonify({"all profiles": profiles}), 200)

def get_user_profile(userId: int):

    
    user_profile = profile.get_profile_by_id(int(userId))

    if user_profile:
        return make_response(jsonify({"profile": user_profile, "msg": "SUCCESS"}), 200)
    
    return make_response(jsonify({"profile": None, "msg": 'profile not found'}), 404)

def update_user_profile(profileId: int):
    data = request.get_json()
    updated_profile = profile.update_profile(profileId, **data)

    if updated_profile is None:
        return make_response(
            jsonify({
                "status": "Profile not found",
                "status_code": 404,
                "message": "Profile not found",
                "errors": [{"field": "Profile not found", "error": "Profile not found"}]
            }),
            404
        )

    return make_response(jsonify({"updated_profile": updated_profile, "msg": "SUCCESS"}), 200)