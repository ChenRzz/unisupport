from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from repo.userRepo import UserRepository


class LoginService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username_or_email: str, password: str) -> tuple[bool, str, dict]:
        """
        Authenticate the user and generate a JWT token

        Args:
            username_or_email (str): Username or email
            password (str): Password

        Returns:
            tuple: (Success status, Message, Data)
        """
        # Print debug information
        print(f"Login attempt: {username_or_email}")

        # Try to find the user by email first
        user = self.user_repo.get_user_by_email(username_or_email)
        print(f"Lookup by email result: {user}")

        if not user:
            # If not found by email, try username
            user = self.user_repo.get_user_by_username(username_or_email)
            print(f"Lookup by username result: {user}")

        if not user:
            return False, "User does not exist", {}

        # Print password information
        print(f"Password hash in DB: {user.password_hash}")
        print(f"Input password: {password}")

        # Verify password
        if not check_password_hash(user.password_hash, password):
            return False, "Incorrect password", {}

        # Create JWT token with expiration and extra claims
        access_token = create_access_token(
            identity=str(user.id),  # Convert user ID to string
            additional_claims={
                "username": user.username,
                "email": user.email,
                "is_stuff": user.is_stuff
            }
        )

        return True, "Login successful", {
            "access_token": access_token,
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }

    def create_user(self, username: str, email: str, password: str, is_stuff: bool = False) -> tuple[bool, str, dict]:
        """
        Create a new user
        Args:
            username: Username
            email: Email
            password: Password
            is_stuff: Is admin
        Returns:
            tuple: (Success status, Message, Data)
        """
        # Check if username already exists
        if self.user_repo.get_user_by_username(username):
            return False, "Username already exists", {}

        # Check if email is already registered
        if self.user_repo.get_user_by_email(email):
            return False, "Email already registered", {}

        try:
            user = self.user_repo.create_user(
                username=username,
                email=email,
                password=password,
                is_stuff=is_stuff
            )

            return True, "User created successfully", {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_stuff": user.is_stuff
            }
        except Exception as e:
            return False, f"Failed to create user: {str(e)}", {}

    def change_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        Change user password
        Args:
            user_id: User ID
            old_password: Old password
            new_password: New password
        Returns:
            tuple: (Success status, Message)
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return False, "User does not exist"

        if not check_password_hash(user.password_hash, old_password):
            return False, "Incorrect old password"

        try:
            self.user_repo.update_password(user_id, new_password)
            return True, "Password changed successfully"
        except Exception as e:
            return False, f"Failed to change password: {str(e)}"