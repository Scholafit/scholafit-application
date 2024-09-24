from app.models.user import User
from app.models.database import db

def create_user(data):
    """
    Create a new user with the provided data.
    Args:
        data (dict): A dictionary containing user details (firstname, lastname, email, password).
    Returns:
        str: A success message or error message.
    """
    try:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return {"message": "User created successfully", "user": user.to_dict()}
    except Exception as e:
        return f"Error creating user: {str(e)}"


def get_user():
    """
    Fetch all users from the database.
    Returns:
        list: A list of all users in dictionary format.
    """
    return User.all_users()

def get_user_by_email(email):
    """Fetch a user by their email."""
    user = User.find_by_email(email)
    if user:
        return user.to_dict()
    return None

def delete_user_by_email(email):
    """Delete a user by their email."""
    user = User.find_by_email(email)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
