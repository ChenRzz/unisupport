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
    is_stuff = Column(Boolean, default=False)  # True if the user is staff/admin
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships - use string references
    questionnaires = relationship("UserQuestionnaire", back_populates="user", lazy="dynamic")

    # These will be enabled when internal course features are implemented
    # enrolled_courses = relationship("CourseUser", back_populates="user", lazy="dynamic")
    # assignments = relationship("UserAssignment", back_populates="user", lazy="dynamic")

    # Task relationship - use string references
    tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan")

    # Add major relationship field
    major_id = Column(Integer, ForeignKey('majors.id'), nullable=True)
    major = relationship("Major", backref="users")
