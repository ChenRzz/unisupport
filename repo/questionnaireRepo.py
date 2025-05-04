from sqlalchemy.orm import Session, joinedload
from model.questionnaire import Questionnaire, UserQuestionnaire

class QuestionnaireRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_questionnaires(self):
        """Retrieve all questionnaires"""
        return self.session.query(Questionnaire).all()

    def get_questionnaire_by_id(self, questionnaire_id: int):
        """Retrieve a questionnaire by its ID"""
        return self.session.query(Questionnaire).get(questionnaire_id)

    def get_user_questionnaires(self, user_id: int):
        """Retrieve all questionnaire records for a given user"""
        return (
            self.session.query(UserQuestionnaire)
            .filter_by(user_id=user_id)
            .join(UserQuestionnaire.questionnaire)
            .all()
        )

    def get_shared_questionnaires(self):
        """Retrieve all shared questionnaire records"""
        return (
            self.session.query(UserQuestionnaire)
            .filter_by(is_shared=True)
            .join(UserQuestionnaire.questionnaire)
            .join(UserQuestionnaire.user)
            .all()
        )

    def get_user_questionnaire_by_id(self, record_id: int):
        """Retrieve a user questionnaire record by its ID"""
        return self.session.query(UserQuestionnaire).get(record_id)

    def create_user_questionnaire(self, user_questionnaire: UserQuestionnaire):
        """Create a user questionnaire record"""
        try:
            self.session.add(user_questionnaire)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def delete_user_questionnaire(self, record: UserQuestionnaire):
        """Delete a user questionnaire record"""
        try:
            self.session.delete(record)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise e

    def get_questionnaire_by_type(self, type: str):
        """Retrieve a questionnaire by its type"""
        try:
            return self.session.query(Questionnaire).filter(Questionnaire.type == type).first()
        except Exception as e:
            print(f"Failed to retrieve questionnaire: {str(e)}")
            return None

    def create_questionnaire(self, questionnaire: Questionnaire):
        """Create a new questionnaire"""
        try:
            self.session.add(questionnaire)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Failed to create questionnaire: {str(e)}")
            return False
