from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
import datetime
from model.db_base import Base

# Questionnaire table
class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False)  # Questionnaire type
    description = Column(Text)  # Description of the questionnaire
    content = Column(JSON, nullable=False)  # Question content stored as JSON
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    user_questionnaires = relationship("UserQuestionnaire", back_populates="questionnaire")


# User questionnaire record table
class UserQuestionnaire(Base):
    __tablename__ = 'user_questionnaires'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    questionnaire_id = Column(Integer, ForeignKey('questionnaires.id'), nullable=False)
    assessment = Column(JSON, nullable=False)  # User's answers or scoring results
    is_shared = Column(Boolean, default=False)  # Whether the record is publicly shared
    is_problematic = Column(Boolean, default=False)  # Flag if responses indicate a concern
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    questionnaire = relationship("Questionnaire", back_populates="user_questionnaires")
    user = relationship("User", back_populates="questionnaires")
