import unittest
import json
from unittest.mock import patch
from app import create_app
from model.db_base import Base, engine, session
from werkzeug.security import generate_password_hash
from datetime import datetime
from model.user import User
from model.questionnaire import Questionnaire, UserQuestionnaire
from model.resource import Major, ResourceType, OnlineCourse, Paper, Seminar, MajorResource
from model.task import Task, UserTask, TaskStatus, TaskPriority, TaskType

class TestAPIIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up the test environment"""
        # Create test app
        cls.app = create_app()
        cls.client = cls.app.test_client()
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Patch only what is necessary to avoid import issues
        cls.login_service_patcher = patch('app.controllers.user_controller.LoginService')
        cls.mock_login_service = cls.login_service_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment"""
        cls.app_context.pop()
        cls.login_service_patcher.stop()

    def test_login_page(self):
        """Test loading of the login page"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'UniSupport', response.data)

    def test_unauthorized_access(self):
        """Test unauthorized access - note: should return 401 instead of 302"""
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()
