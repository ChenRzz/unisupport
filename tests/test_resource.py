import unittest
from unittest.mock import MagicMock, patch
from core.resource import ResourceService
from core.resource_recommender import ResourceRecommender
from model.resource import Major, MajorResource, ResourceType, OnlineCourse, Paper, Seminar
from model.user import User


class TestResourceService(unittest.TestCase):
    def setUp(self):
        # Create mocked resource and questionnaire repositories
        self.resource_repo_mock = MagicMock()
        self.questionnaire_repo_mock = MagicMock()

        # Create test user
        self.test_user = User()
        self.test_user.id = 1
        self.test_user.username = "testuser"
        self.test_user.major_id = 1

        # Create test major - updated to actual major name
        self.test_major = Major()
        self.test_major.id = 1
        self.test_major.name = "Computer Science and Technology"
        self.test_major.description = "This major prepares professionals with capabilities in both hardware and software design and development."

        # Create test resource - updated to actual course name
        self.test_course = OnlineCourse()
        self.test_course.id = 1
        self.test_course.name = "Data Structures and Algorithms"
        self.test_course.description = "Introduces basic data structures and algorithm design methods including sorting, searching, and graph algorithms."
        self.test_course.instructor = "Professor Zhang"

        # Configure mocked repository behavior
        self.resource_repo_mock.get_major_by_id.return_value = self.test_major
        self.resource_repo_mock.get_major_resources.return_value = []

        # Create service instance
        self.resource_service = ResourceService(self.resource_repo_mock, self.questionnaire_repo_mock)

    def test_get_major_resources_success(self):
        """Positive test: successfully retrieve major resources"""
        result, error = self.resource_service.get_major_resources(1)

        self.assertIsNone(error)
        self.assertEqual(result["major"], self.test_major)
        self.assertIn("resources", result)

    def test_get_major_resources_not_found(self):
        """Negative test: major not found"""
        self.resource_repo_mock.get_major_by_id.return_value = None

        result, error = self.resource_service.get_major_resources(999)

        self.assertIsNone(result)
        self.assertEqual(error, "Major not found")

    @patch.object(ResourceRecommender, 'get_personalized_recommendations')
    def test_get_personalized_recommendations_success(self, mock_get_recommendations):
        """Positive test: successfully get personalized recommendations"""
        mock_get_recommendations.return_value = {
            'online_courses': [self.test_course],
            'papers': [],
            'seminars': []
        }

        recommendations, error = self.resource_service.get_personalized_recommendations(self.test_user)

        self.assertIsNone(error)
        self.assertEqual(recommendations['online_courses'], [self.test_course])
        mock_get_recommendations.assert_called_once_with(self.test_user)

    def test_get_personalized_recommendations_no_recommender(self):
        """Negative test: recommendation service not initialized"""
        resource_service = ResourceService(self.resource_repo_mock)

        recommendations, error = resource_service.get_personalized_recommendations(self.test_user)

        self.assertIsNone(recommendations)
        self.assertEqual(error, "Recommendation service not initialized")


if __name__ == '__main__':
    unittest.main()
