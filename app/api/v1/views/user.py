from . import app_views
from app.models.user import user  # Import the `user` object which is an instance of the User class
from flask import request, jsonify

# Create a user
@app_views.route('/users', methods=['POST'])
def create_user_route():
    try:
        user_data = request.get_json()
        new_user = user.create_user(**user_data)
        return jsonify(new_user), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get a user by ID
@app_views.route('/users/<int:user_id>', methods=['GET'])
def get_user_route(user_id):
    try:
        user_data = user.get_user_by_id(user_id)
        if user_data:
            return jsonify(user_data), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Update a user
@app_views.route('/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    try:
        update_data = request.get_json()
        updated_user = user.update_user(user_id, **update_data)
        if updated_user:
            return jsonify(updated_user), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Delete a user
@app_views.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    try:
        if user.delete_user(user_id):
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all users
@app_views.route('/users', methods=['GET'])
def get_all_users_route():
    try:
        users = user.get_all()  # Call the get_all method on the `user` instance
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
