from repo.questionnaireRepo import QuestionnaireRepository
from model.questionnaire import UserQuestionnaire
class QuestionnaireService:
    def __init__(self, questionnaire_repo: QuestionnaireRepository):
        self.questionnaire_repo = questionnaire_repo

    def get_questionnaires(self):
        """get all questionnaires"""
        return self.questionnaire_repo.get_all_questionnaires()

    def get_questionnaire(self, questionnaire_id: int):
        """get a questionnaire"""
        return self.questionnaire_repo.get_questionnaire_by_id(questionnaire_id)

    def get_user_questionnaires(self, user_id: int):
        """get all user questionnaires record"""
        return self.questionnaire_repo.get_user_questionnaires(user_id)

    def get_shared_questionnaires(self):
        """get all questionaries history"""
        return self.questionnaire_repo.get_shared_questionnaires()

    def submit_questionnaire(self, user_id: int, questionnaire_id: int, answers: dict, is_shared: bool):
        pass

    def delete_questionnaire_record(self, record_id: int, user_id: int):
