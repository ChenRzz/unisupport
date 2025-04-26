from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from repo.userRepo import UserRepository


class LoginService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate(self, username_or_email: str, password: str) -> tuple[bool, str, dict]:
        """
        验证用户身份并生成JWT令牌

        Args:
            username_or_email (str): 用户名或邮箱
            password (str): 密码

        Returns:
            tuple: (是否成功, 消息, 数据)
        """
        # 打印调试信息
        print(f"尝试登录: {username_or_email}")

        # 先尝试通过邮箱查找用户
        user = self.user_repo.get_user_by_email(username_or_email)
        print(f"通过邮箱查找结果: {user}")

        if not user:
            # 如果邮箱未找到，尝试通过用户名查找
            user = self.user_repo.get_user_by_username(username_or_email)
            print(f"通过用户名查找结果: {user}")

        if not user:
            return False, "用户不存在", {}

        # 打印密码信息
        print(f"数据库密码哈希: {user.password_hash}")
        print(f"输入的密码: {password}")

        # 验证密码
        if not check_password_hash(user.password_hash, password):
            return False, "密码错误", {}

        # 创建JWT Token，设置过期时间和额外信息
        access_token = create_access_token(
            identity=str(user.id),  # 将用户ID转换为字符串
            additional_claims={
                "username": user.username,
                "email": user.email,
                "is_stuff": user.is_stuff
            }
        )

        return True, "登录成功", {
            "access_token": access_token,
            "user_id": user.id,
            "username": user.username,
            "email": user.email
        }

    def create_user(self, username: str, email: str, password: str, is_stuff: bool = False) -> tuple[bool, str, dict]:
        """
        创建新用户
        Args:
            username: 用户名
            email: 邮箱
            password: 密码
            is_stuff: 是否为管理员
        Returns:
            tuple: (是否成功, 消息, 数据)
        """
        # 检查用户名是否已存在
        if self.user_repo.get_user_by_username(username):
            return False, "用户名已存在", {}

        # 检查邮箱是否已存在
        if self.user_repo.get_user_by_email(email):
            return False, "邮箱已被注册", {}

        try:
            user = self.user_repo.create_user(
                username=username,
                email=email,
                password=password,
                is_stuff=is_stuff
            )

            return True, "用户创建成功", {
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
                "is_stuff": user.is_stuff
            }
        except Exception as e:
            return False, f"创建用户失败: {str(e)}", {}

    def change_password(self, user_id: int, old_password: str, new_password: str) -> tuple[bool, str]:
        """
        修改用户密码
        Args:
            user_id: 用户ID
            old_password: 旧密码
            new_password: 新密码
        Returns:
            tuple: (是否成功, 消息)
        """
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return False, "用户不存在"

        if not check_password_hash(user.password_hash, old_password):
            return False, "原密码错误"

        try:
            self.user_repo.update_password(user_id, new_password)
            return True, "密码修改成功"
        except Exception as e:
            return False, f"密码修改失败: {str(e)}"
