from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from repo.userRepo import UserRepository
class LoginService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
    def authenticate(self, username_or_email: str, password: str) -> tuple[bool, str, dict]:
        pass

    def create_user(self, username: str, email: str, password: str, is_stuff: bool = False) -> tuple[bool, str, dict]:
        pass

    def change_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        pass


