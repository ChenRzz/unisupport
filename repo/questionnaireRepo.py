from sqlalchemy.orm import Session, joinedload
from model.questionnaire import Questionnaire, UserQuestionnaire

class QuestionnaireRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_questionnaires(self):
        """获取所有问卷"""
        return self.session.query(Questionnaire).all()

    def get_questionnaire_by_id(self, questionnaire_id: int):
        """根据ID获取问卷"""
        return self.session.query(Questionnaire).get(questionnaire_id)

    def get_user_questionnaires(self, user_id: int):
        """获取用户的问卷记录"""
        return (self.session.query(UserQuestionnaire)
                .filter_by(user_id=user_id)
                .join(UserQuestionnaire.questionnaire)
                .all())