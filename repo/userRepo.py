from typing import Optional
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash
from model.user import User
import datetime

class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        Retrieve a user by email.

        Args:
            email (str): User's email address.

        Returns:
            User: The user object if found, otherwise None.
        """
        print(f"Querying email: {email}")
        user = self.db_session.query(User).filter(User.email == email).first()
        print(f"Query result: {user}")
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        Retrieve a user by username.

        Args:
            username (str): The username.

        Returns:
            User: The user object if found, otherwise None.
        """
        print(f"Querying username: {username}")
        user = self.db_session.query(User).filter(User.username == username).first()
        print(f"Query result: {user}")
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve a user by ID."""
        return self.db_session.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, email: str, password: str, is_stuff: bool = False) -> User:
        """
        Create a new user.

        Args:
            username (str): The username.
            email (str): The email address.
            password (str): The plain text password.
            is_stuff (bool): Whether the user is staff (admin).

        Returns:
            User: The newly created user object.
        """
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            is_stuff=is_stuff,
            created_at=datetime.datetime.utcnow(),
            updated_at=datetime.datetime.utcnow()
        )

        self.db_session.add(user)
        self.db_session.commit()
        return user

    def update_password(self, user_id: int, new_password: str) -> bool:
        """
        Update the password of an existing user.

        Args:
            user_id (int): The user ID.
            new_password (str): The new password in plain text.

        Returns:
            bool: True if successful, False if user not found.
        """
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.password_hash = generate_password_hash(new_password)
        user.updated_at = datetime.datetime.utcnow()
        self.db_session.commit()
        return True
