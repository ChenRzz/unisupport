import unittest
from unittest.mock import MagicMock, patch
from werkzeug.security import generate_password_hash
from core.login import LoginService
from model.user import User


class TestLoginService(unittest.TestCase):
    def setUp(self):
        # Create a mocked user repository
        self.user_repo_mock = MagicMock()

        # Create a test user (same as 'student' in user_data.py)
        self.test_user = User()
        self.test_user.id = 2  # ID 2 for student (admin is 1)
        self.test_user.username = "student"
        self.test_user.email = "student@unisupport.com"
        self.test_user.password_hash = generate_password_hash("student123")

        # Configure repository behavior
        self.user_repo_mock.get_user_by_email.return_value = self.test_user
        self.user_repo_mock.get_user_by_username.return_value = self.test_user

        # Create the service instance and mock token creation
        self.login_service = LoginService(self.user_repo_mock)
        self.login_service._create_token = MagicMock(return_value="mocked_token")

    @patch('core.login.create_access_token')
    def test_authenticate_success(self, mock_create_token):
        """Positive test: authenticate with correct credentials"""
        mock_create_token.return_value = "mocked_token"

        success, message, auth_data = self.login_service.authenticate("student@unisupport.com", "student123")

        self.assertTrue(success)
        self.assertEqual(message, "Login successful")
        self.assertEqual(auth_data["user_id"], 2)
        self.assertEqual(auth_data["username"], "student")
        self.assertEqual(auth_data["email"], "student@unisupport.com")
        self.assertIn("access_token", auth_data)

    def test_authenticate_wrong_password(self):
        """Negative test: wrong password"""
        success, message, auth_data = self.login_service.authenticate("student@unisupport.com", "wrongpassword")

        self.assertFalse(success)
        self.assertEqual(message, "Incorrect password")
        self.assertEqual(auth_data, {})

    def test_authenticate_user_not_found(self):
        """Negative test: user not found"""
        self.user_repo_mock.get_user_by_email.return_value = None
        self.user_repo_mock.get_user_by_username.return_value = None

        success, message, auth_data = self.login_service.authenticate("nonexistent@example.com", "password123")

        self.assertFalse(success)
        self.assertEqual(message, "User does not exist")
        self.assertEqual(auth_data, {})


if __name__ == '__main__':
    unittest.main()
