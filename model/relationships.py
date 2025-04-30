from sqlalchemy.orm import relationship


def setup_relationships():
    from model.user import User
    from model.task import UserTask
    from model.questionnaire import UserQuestionnaire

    # 设置User的关系
    User.questionnaires = relationship("UserQuestionnaire", back_populates="user", lazy="dynamic")
    User.tasks = relationship("UserTask", back_populates="user", cascade="all, delete-orphan") 