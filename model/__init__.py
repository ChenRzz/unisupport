from model.db_base import Base, engine, session
from model.user import User
from model.task import Task, UserTask
from model.questionnaire import Questionnaire, UserQuestionnaire
from model.resource import Paper, OnlineCourse, Seminar, Major, MajorResource
from model.relationships import setup_relationships

# 设置关系
setup_relationships() 