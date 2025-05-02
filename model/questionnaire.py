from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
import datetime
from model.db_base import Base

class Questionnaire(Base):
    __tablename__ = 'questionnaires'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String(100), nullable=False)
    description = Column(Text)
    content = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # 关系定义
    user_questionnaires = relationship("UserQuestionnaire", back_populates="questionnaire")


# 用户问卷表
class UserQuestionnaire(Base):
    __tablename__ = 'user_questionnaires'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    questionnaire_id = Column(Integer, ForeignKey('questionnaires.id'), nullable=False)
    assessment = Column(JSON, nullable=False)
    is_shared = Column(Boolean, default=False)
    is_problematic = Column(Boolean, default=False)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)

    # 关系定义
    questionnaire = relationship("Questionnaire", back_populates="user_questionnaires")
    user = relationship("User", back_populates="questionnaires")
