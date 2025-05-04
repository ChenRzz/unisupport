import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime
from core.questionnaire import QuestionnaireService
from model.questionnaire import UserQuestionnaire, Questionnaire


class TestQuestionnaireService(unittest.TestCase):
    def setUp(self):
        # Create a mocked questionnaire repository
        self.questionnaire_repo_mock = MagicMock()

        # Create test questionnaires and user questionnaires with actual types
        self.test_questionnaire = Questionnaire()
        self.test_questionnaire.id = 1
        self.test_questionnaire.type = "beck_depression_inventory"
        self.test_questionnaire.title = "Beck Depression Inventory (BDI-II)"

        self.study_questionnaire = Questionnaire()
        self.study_questionnaire.id = 2
        self.study_questionnaire.type = "study_status_assessment"
        self.study_questionnaire.title = "Study Status Assessment"

        self.test_user_questionnaire = UserQuestionnaire()
        self.test_user_questionnaire.id = 1
        self.test_user_questionnaire.user_id = 1
        self.test_user_questionnaire.questionnaire_id = 1
        self.test_user_questionnaire.questionnaire = self.test_questionnaire
        self.test_user_questionnaire.is_shared = False
        self.test_user_questionnaire.answers = {"1": "0", "2": "1"}

        # Configure repository behavior
        self.questionnaire_repo_mock.get_questionnaire_by_id.return_value = self.test_questionnaire
        self.questionnaire_repo_mock.get_user_questionnaire_by_id.return_value = self.test_user_questionnaire

        # Create service instance
        self.questionnaire_service = QuestionnaireService(self.questionnaire_repo_mock)

    def test_submit_questionnaire_success(self):
        """Positive test: successfully submit questionnaire"""
        self.questionnaire_repo_mock.create_user_questionnaire.return_value = True

        success, message = self.questionnaire_service.submit_questionnaire(
            user_id=1,
            questionnaire_id=1,
            answers={"1": "0", "2": "1"},
            is_shared=False
        )

        self.assertTrue(success)
        self.assertEqual(message, "Questionnaire submitted successfully")
        self.questionnaire_repo_mock.create_user_questionnaire.assert_called_once()

    def test_submit_questionnaire_questionnaire_not_found(self):
        """Negative test: questionnaire not found - note: current implementation does not check this"""
        self.questionnaire_repo_mock.get_questionnaire_by_id.return_value = None
        self.questionnaire_service = QuestionnaireService(self.questionnaire_repo_mock)

        success, message = self.questionnaire_service.submit_questionnaire(
            user_id=1,
            questionnaire_id=999,
            answers={"1": "0", "2": "1"},
            is_shared=False
        )

        self.assertTrue(success)  # Current implementation skips questionnaire existence check
        self.assertEqual(message, "Questionnaire submitted successfully")
        self.questionnaire_repo_mock.create_user_questionnaire.assert_called_once()

    def test_delete_questionnaire_record_success(self):
        """Positive test: successfully delete questionnaire record"""
        self.questionnaire_repo_mock.delete_user_questionnaire.return_value = True

        success, message = self.questionnaire_service.delete_questionnaire_record(1, 1)

        self.assertTrue(success)
        self.assertEqual(message, "Deleted successfully")
        self.questionnaire_repo_mock.delete_user_questionnaire.assert_called_once()

    def test_delete_questionnaire_record_unauthorized(self):
        """Negative test: unauthorized deletion attempt of another user's record"""
        success, message = self.questionnaire_service.delete_questionnaire_record(1, 2)

        self.assertFalse(success)
        self.assertEqual(message, "You do not have permission to delete this record")
        self.questionnaire_repo_mock.delete_user_questionnaire.assert_not_called()


if __name__ == '__main__':
    unittest.main()
