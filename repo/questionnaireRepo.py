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

    def get_shared_questionnaires(self):
        """获取共享的问卷记录"""
        return self.questionnaire_repo.get_shared_questionnaires()

    def submit_questionnaire(self, user_id: int, questionnaire_id: int, answers: dict, is_shared: bool):
        """提交问卷"""
        try:
            # 创建用户问卷记录
            user_questionnaire = UserQuestionnaire(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                assessment=answers,
                is_shared=is_shared
            )

            # 保存记录
            self.questionnaire_repo.create_user_questionnaire(user_questionnaire)
            return True, "问卷提交成功"
        except Exception as e:
            return False, f"提交失败: {str(e)}"
