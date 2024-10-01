from ..services.secure_pass import verify_password, hash_password
from flask import session
from .user import UserRepository, DB_User
from .database import get_db
from itsdangerous import URLSafeTimedSerializer
import os

class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
        

    def login(self, email: str, password: str):
        """
        Authenticate user based on email and password.
        Args:
            email (str): User email.
            password (str): Plain-text password.
        Returns:
            dict: A success message or error message.
        """
        # Query to find the user by email
        specific_user = self.user_repo.database.session.query(DB_User).filter_by(email=email).first()

        # Validate the user and password
        if specific_user and verify_password(password, specific_user.password):
            session['user_id'] = specific_user.id  # Set session to track user login
            return {"message": "Login successful", "user": specific_user.to_dict()}
        return {"error": "Invalid credentials"}

    def logout(self):
        """Log out the user by clearing the session."""
        session.pop('user_id', None)
        return {"message": "Logged out successfully"}

    def is_authenticated(self):
        """Check if a user is authenticated by checking the session."""
        return 'user_id' in session
    
    def forgot_password(self, email: str):
        """Send a password reset token to the user's email."""
        user = self.user_repo.database.session.query(DB_User).filter_by(email=email).first()
        if user:
            token = self.serializer.dumps(email, salt='password-reset-salt')
            #reset_link = f"{current_app.config['FRONTEND_URL']}/reset-password/{token}"
            #send_email(user.email, reset_link)  # Function to send the email
            return token
        return {"error": "Email not found."}

    def reset_password(self, token: str, new_password: str):
        """Reset the user's password using the token."""
        try:
            email = self.serializer.loads(token, salt='password-reset-salt', max_age=3600)
            user = self.user_repo.database.session.query(DB_User).filter_by(email=email).first()
            if user:
                user.password = hash_password(new_password)
                self.user_repo.database.session.commit()
                return {"message": "Password has been updated successfully."}
            return {"error": "User not found."}
        except Exception as e:
            return {"error": "Invalid or expired token."}

# Initialize database and repository
database = get_db()
user_repository = UserRepository(database)
auth_service = AuthService(user_repository)