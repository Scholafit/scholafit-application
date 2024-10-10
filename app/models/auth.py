from ..services.secure_pass import verify_password, hash_password
from flask import session
from .user import UserRepository, DB_User
from .database import get_db
from itsdangerous import URLSafeTimedSerializer
import os
from ..services.notification import create_email_notification_service


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repo = user_repository
        self.serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
        

    def login(self, identifier: str, password: str):
        """
        Authenticate user based on email and password.
        Args:
            email (str): User email.
            password (str): Plain-text password.
        Returns:
            dict: A success message or error message.
        """
        # Query to find the user by email or username
        specific_user = self.user_repo.database.session.query(DB_User).filter((DB_User.email == identifier) | (DB_User.username == identifier)).first()

        # Validate the user and password
        if specific_user and verify_password(password, specific_user.password):
            session['user_id'] = specific_user.id
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

            #Sends the password reset link to the user's email
            reset_link = f"127.0.0.1:5000/api/v1/reset-password/{token}"
            subject = "Password Reset Link"
            message = f"Please use the following link to rest your password: {reset_link}"
            sender_address = "info@scholafit.com"
            email_service = create_email_notification_service(sender_address)
            email_service.notify(user.email, message, subject)

            return {"message": "Password reset link sent to your email."}
    
        return {"error": "Email not found."}

    def reset_password(self, token: str, new_password: str):
        """Reset the user's password using the token."""
        try:
            email = self.serializer.loads(token, salt='password-reset-salt', max_age=7200)
            user = self.user_repo.database.session.query(DB_User).filter_by(email=email).first()
            if user:
                user.password = hash_password(new_password)
                self.user_repo.database.session.commit()

                # Email to notify the user that the password reset was sucessful
                subject = "Password Reset"
                message = "Your Password Reset was sucessful, Login to your account with your new paasword"
                sender_address = "info@scholafit.com"
                email_service = create_email_notification_service(sender_address)
                email_service.notify(user.email, message, subject)

                # Return a sucess message to user screen
                return {"message": "Password has been updated successfully."}
            
            #Return if the user email was not found
            return {"error": "User not found."}
        except Exception as e:
            return {"error": "Invalid or expired token."}
        
    def verify_user(self, token: str):
        """
        Verify a user based on the provided token.
        Args:
            token (str): The verification token.
        Returns:
            dict: A message indicating the status of verification or an error message.
        """
        try:
            # Decrypt the token to get the email
            email = self.serializer.loads(token, salt='verify-email-salt', max_age=3600)
        except Exception as e:
            return {"error": "Invalid or expired token."}

        # Fetch the user by email
        user = self.user_repo.database.session.query(DB_User).filter_by(email=email).first()
        if not user:
            return {"error": "User not found."}

        # Update the `is_verified` field to True
        user.is_verified = True
        self.user_repo.database.session.commit()

        #Notify a user about the sucess of the verification of account
        subject = "Welcome"
        message = "Welcome to Scholafit, you have successfully verified your account"
        sender_address = "info@scholafit.com"
        email_service = create_email_notification_service(sender_address)
        email_service.notify(user.email, message, subject)
        return {"message": "User verified successfully."}

# Initialize database and repository
database = get_db()
user_repository = UserRepository(database)
auth_service = AuthService(user_repository)