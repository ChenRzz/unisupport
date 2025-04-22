from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from repo.userRepo import UserRepository
class UserRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session
