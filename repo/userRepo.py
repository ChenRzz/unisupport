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
        通过邮箱获取用户

        Args:
            email (str): 用户邮箱

        Returns:
            User: 用户对象，如果不存在则返回None
        """
        print(f"查询邮箱: {email}")
        user = self.db_session.query(User).filter(User.email == email).first()
        print(f"查询结果: {user}")
        return user

    def get_user_by_username(self, username: str) -> Optional[User]:
        """
        通过用户名获取用户

        Args:
            username (str): 用户名

        Returns:
            User: 用户对象，如果不存在则返回None
        """
        print(f"查询用户名: {username}")
        user = self.db_session.query(User).filter(User.username == username).first()
        print(f"查询结果: {user}")
        return user

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db_session.query(User).filter(User.id == user_id).first()

    def create_user(self, username: str, email: str, password: str, is_stuff: bool = False) -> User:
        """创建新用户"""
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
        """更新用户密码"""
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        user.password_hash = generate_password_hash(new_password)
        user.updated_at = datetime.datetime.utcnow()
        self.db_session.commit()
        return True