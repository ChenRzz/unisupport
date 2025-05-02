from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import datetime
from model.db_base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password_hash = Column(String(128), nullable=False)
    is_stuff = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 关系定义 - 使用字符串引用
    questionnaires = relationship("UserQuestionnaire", back_populates="user", lazy="dynamic")
    # 暂时注释掉这两行，等到实现校内课程功能时再启用
    # enrolled_courses = relationship("CourseUser", back_populates="user", lazy="dynamic")
    # assignments = relationship("UserAssignment", back_populates="user", lazy="dynamic")

    # 添加任务关联 - 使用字符串引用
    tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan")

    # 添加专业字段
    major_id = Column(Integer, ForeignKey('majors.id'), nullable=True)
    major = relationship("Major", backref="users")