from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
import datetime
import enum
from model.db_base import Base
from model.user import User  # Now safe to import User


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
    EXAM = "exam"  # Exam
    HOMEWORK = "homework"  # Homework
    CUSTOM = "custom"  # Custom task created by the user


class TaskStatus(enum.Enum):
    TODO = "todo"  # To do
    IN_PROGRESS = "in_progress"  # In progress
    COMPLETED = "completed"  # Completed


# Internal course-related models are temporarily disabled
# class Assignment(Base):
#     ...

# class UserAssignment(Base):
#     ...

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)  # Task title
    description = Column(String(500))  # Task description
    due_date = Column(DateTime)  # Deadline
    priority = Column(Enum(TaskPriority), nullable=False)  # Priority level
    type = Column(Enum(TaskType), nullable=False)  # Task type
    is_system_task = Column(Boolean, default=False)  # System-generated task
    course_name = Column(String(100))  # Related course name
    external_url = Column(String(200))  # External reference link
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user_tasks = relationship("UserTask", back_populates="task", cascade="all, delete-orphan")  # Linked user tasks


class UserTask(Base):
    __tablename__ = 'user_tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Reference to user
    task_id = Column(Integer, ForeignKey('tasks.id'), nullable=False)  # Reference to task
    status = Column(Enum(TaskStatus), nullable=False, default=TaskStatus.TODO)  # Task status
    notes = Column(String(500))  # Personal notes
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    user = relationship("User", back_populates="tasks")
    task = relationship("Task", back_populates="user_tasks")
