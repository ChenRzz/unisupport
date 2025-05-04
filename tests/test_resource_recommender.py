import unittest
from unittest.mock import MagicMock, patch
from core.resource_recommender import ResourceRecommender
from model.resource import Major, MajorResource, ResourceType, OnlineCourse, Paper, Seminar
from model.user import User
from model.questionnaire import UserQuestionnaire, Questionnaire


class TestResourceRecommender(unittest.TestCase):
    def setUp(self):
        # Create mocked repositories
        self.resource_repo_mock = MagicMock()
        self.questionnaire_repo_mock = MagicMock()

        # Create a test user
        self.test_user = User()
        self.test_user.id = 1
        self.test_user.username = "testuser"
        self.test_user.major_id = 1

        # Create test course - adjusted to actual data
        self.test_course = OnlineCourse()
        self.test_course.id = 1
        self.test_course.name = "Data Structures and Algorithms"
        self.test_course.description = "Covers basic data structures and algorithm design, including sorting, searching, and graph algorithms."
        self.test_course.instructor = "Professor Zhang"
        self.test_course.duration = "48 hours"

        # Create test paper - adjusted to actual data
        self.test_paper = Paper()
        self.test_paper.id = 1
        self.test_paper.title = "Applications of AI in Software Testing"
        self.test_paper.authors = "Researcher Wang, Researcher Zhang"
        self.test_paper.publication = "Journal of Software Engineering"

        # Set repository behaviors
        self.resource_repo_mock.get_major_resources.return_value = [
            MagicMock(resource_type=ResourceType.ONLINE_COURSE, resource_id=1)
        ]
        self.resource_repo_mock.get_online_course.return_value = self.test_course
        self.resource_repo_mock.get_popular_online_courses.return_value = [self.test_course]
        self.resource_repo_mock.get_popular_papers.return_value = [self.test_paper]
        self.resource_repo_mock.get_popular_seminars.return_value = []

        # Set questionnaire repository behavior
        self.questionnaire_repo_mock.get_user_questionnaires.return_value = []

        # Create recommender instance
        self.recommender = ResourceRecommender(self.resource_repo_mock, self.questionnaire_repo_mock)

    def test_get_personalized_recommendations_with_major(self):
        """Positive case: get personalized recommendations based on user's major"""
        recommendations = self.recommender.get_personalized_recommendations(self.test_user)

        self.assertIn('online_courses', recommendations)
        self.assertIn('papers', recommendations)
        self.assertIn('seminars', recommendations)
        self.assertEqual(len(recommendations['online_courses']), 1)
        self.assertEqual(recommendations['online_courses'][0], self.test_course)

    def test_get_personalized_recommendations_without_major(self):
        """Positive case: personalized recommendations without major should fallback to popular resources"""
        user_without_major = User()
        user_without_major.id = 2
        user_without_major.username = "testuser2"
        user_without_major.major_id = None

        recommendations = self.recommender.get_personalized_recommendations(user_without_major)

        self.assertIn('online_courses', recommendations)
        self.assertIn('papers', recommendations)
        self.assertIn('seminars', recommendations)
        self.assertEqual(len(recommendations['online_courses']), 1)
        self.assertEqual(len(recommendations['papers']), 1)
        self.assertEqual(recommendations['online_courses'][0], self.test_course)
        self.assertEqual(recommendations['papers'][0], self.test_paper)

    def test_fill_popular_recommendations(self):
        """Positive case: fill popular resources when recommendation list is insufficient"""
        recommendations = {
            'online_courses': [],
            'papers': [],
            'seminars': []
        }

        self.recommender._fill_popular_recommendations(recommendations, 5)

        self.assertEqual(len(recommendations['online_courses']), 1)
        self.assertEqual(len(recommendations['papers']), 1)
        self.assertEqual(len(recommendations['seminars']), 0)


if __name__ == '__main__':
    unittest.main()
