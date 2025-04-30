from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import datetime
import enum
from model.db_base import Base
from model.user import User  # 现在可以安全导入User


class AssignmentStatus(enum.Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    LATE = "late"
    GRADED = "graded"


class TaskPriority(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskType(enum.Enum):
    EXAM = "exam"  # 考试
    HOMEWORK = "homework"  # 作业
    CUSTOM = "custom"  # 自定义任务


class TaskStatus(enum.Enum):
    TODO = "todo"  # 待完成
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"  # 已完成


# 暂时注释掉校内课程相关的类
# class Assignment(Base):
#     ...

# class UserAssignment(Base):
#     ...

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    due_date = Column(DateTime)
    priority = Column(Enum(TaskPriority), nullable=False)
    type = Column(Enum(TaskType), nullable=False)
    is_system_task = Column(Boolean, default=False)
    course_name = Column(String(100))
    external_url = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_tasks = relationship("UserTask", back_populates="task", cascade="all, delete-orphan")


class UserTask(Base):
    __tablename__ = 'user_tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)
    notes = Column(String(500))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="tasks")
    task = relationship("Task", back_populates="user_tasks")
