from repo.resourceRepo import ResourceRepository
from repo.questionnaireRepo import QuestionnaireRepository
from model.resource import ResourceType
from core.resource_recommender import ResourceRecommender


class ResourceService:
    def __init__(self, resource_repo: ResourceRepository, questionnaire_repo=None):
        self.resource_repo = resource_repo
        self.questionnaire_repo = questionnaire_repo
        if questionnaire_repo:
            self.recommender = ResourceRecommender(resource_repo, questionnaire_repo)
        else:
            self.recommender = None

    def get_all_majors(self):
        """Get all majors"""
        return self.resource_repo.get_all_majors()

    def get_major_resources(self, major_id: int):
        """Get all resources for a major, categorized by type"""
        major = self.resource_repo.get_major_by_id(major_id)
        if not major:
            return None, "Major not found"

        resources = self.resource_repo.get_major_resources(major_id)

        # Categorize resources by type
        categorized_resources = {
            'online_courses': [],
            'papers': [],
            'seminars': []
        }

        for resource in resources:
            if resource.resource_type == ResourceType.ONLINE_COURSE:
                course = self.resource_repo.get_online_course(resource.resource_id)
                if course:
                    categorized_resources['online_courses'].append(course)
            elif resource.resource_type == ResourceType.PAPER:
                paper = self.resource_repo.get_paper(resource.resource_id)
                if paper:
                    categorized_resources['papers'].append(paper)
            elif resource.resource_type == ResourceType.SEMINAR:
                seminar = self.resource_repo.get_seminar(resource.resource_id)
                if seminar:
                    categorized_resources['seminars'].append(seminar)

        return {
            'major': major,
            'resources': categorized_resources
        }, None

    def get_personalized_recommendations(self, user):
        """Get personalized recommendations"""
        if not self.recommender:
            return None, "Recommendation service not initialized"

        try:
            # Debug log
            print(f"Preparing to generate recommendations for user {user.username} (ID: {user.id})")

            # Check user object
            if not hasattr(user, 'major_id'):
                print("Note: The user object does not have a major_id attribute, skipping major-based recommendations")

            recommendations = self.recommender.get_personalized_recommendations(user)
            return recommendations, None
        except Exception as e:
            import traceback
            print(f"Failed to get recommendations: {str(e)}")
            print(traceback.format_exc())  # Print full stack trace
            return None, f"Failed to get recommendations: {str(e)}"