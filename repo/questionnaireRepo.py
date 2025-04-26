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

    def delete_questionnaire_record(self, record_id: int, user_id: int):
        """删除问卷记录"""
        try:
            # 获取记录
            record = self.questionnaire_repo.get_user_questionnaire_by_id(record_id)

            if not record:
                return False, "记录不存在"

            # 验证所有权
            if record.user_id != user_id:
                return False, "无权删除此记录"

            # 删除记录
            self.questionnaire_repo.delete_user_questionnaire(record)
            return True, "删除成功"
        except Exception as e:
            return False, f"删除失败: {str(e)}"