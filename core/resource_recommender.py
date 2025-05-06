from model.resource import ResourceType, OnlineCourse, Paper, Seminar, Major
from model.questionnaire import UserQuestionnaire
from model.user import User
from repo.resourceRepo import ResourceRepository
from repo.questionnaireRepo import QuestionnaireRepository
import random


class ResourceRecommender:
    def __init__(self, resource_repo: ResourceRepository, questionnaire_repo: QuestionnaireRepository):
        self.resource_repo = resource_repo
        self.questionnaire_repo = questionnaire_repo

    def get_personalized_recommendations(self, user: User, limit: int = 5):
        """Get personalized recommended resources"""
        recommendations = {
            'online_courses': [],
            'papers': [],
            'seminars': []
        }

        # Recommendations based on major
        if hasattr(user, 'major_id') and user.major_id:
            major_recommendations = self._get_major_based_recommendations(user.major_id, limit)
            for key in recommendations:
                recommendations[key].extend(major_recommendations.get(key, []))

        # Recommendations based on questionnaire results
        questionnaire_recommendations = self._get_questionnaire_based_recommendations(user.id, limit)
        for key in recommendations:
            # Avoid duplicate recommendations
            existing_ids = [item.id for item in recommendations[key]]
            recommendations[key].extend([
                item for item in questionnaire_recommendations.get(key, [])
                if item.id not in existing_ids
            ])

            # Limit the number of resources per category
            recommendations[key] = recommendations[key][:limit]

        # If recommendations are insufficient, fill in with popular resources
        self._fill_popular_recommendations(recommendations, limit)

        return recommendations

    def _get_major_based_recommendations(self, major_id: int, limit: int):
        """Get recommendations based on major"""
        resources = self.resource_repo.get_major_resources(major_id)

        result = {
            'online_courses': [],
            'papers': [],
            'seminars': []
        }

        for resource in resources:
            if resource.resource_type == ResourceType.ONLINE_COURSE:
                course = self.resource_repo.get_online_course(resource.resource_id)
                if course and course not in result['online_courses']:
                    result['online_courses'].append(course)
            elif resource.resource_type == ResourceType.PAPER:
                paper = self.resource_repo.get_paper(resource.resource_id)
                if paper and paper not in result['papers']:
                    result['papers'].append(paper)
            elif resource.resource_type == ResourceType.SEMINAR:
                seminar = self.resource_repo.get_seminar(resource.resource_id)
                if seminar and seminar not in result['seminars']:
                    result['seminars'].append(seminar)

        # Random selection to avoid always recommending the same resources
        for key in result:
            if len(result[key]) > limit:
                result[key] = random.sample(result[key], limit)

        return result

    def _get_questionnaire_based_recommendations(self, user_id: int, limit: int):
        """Get recommendations based on questionnaire results"""
        user_questionnaires = self.questionnaire_repo.get_user_questionnaires(user_id)
        if not user_questionnaires:
            return {}

        # Sort by creation time and get the latest questionnaire
        latest_questionnaire = sorted(user_questionnaires, key=lambda q: q.created_date, reverse=True)[0]

        result = {
            'online_courses': [],
            'papers': [],
            'seminars': []
        }

        questionnaire_type = latest_questionnaire.questionnaire.type
        assessment = latest_questionnaire.assessment

        # Recommend different resources based on questionnaire type
        if questionnaire_type == 'beck_depression_inventory':
            # Recommend mental health resources for depression inventory
            mental_health_resources = self._get_mental_health_resources()
            for key in result:
                result[key].extend(mental_health_resources.get(key, []))

        elif questionnaire_type == 'study_status_assessment':
            # Recommend study method resources for study status assessment
            study_method_resources = self._get_study_method_resources()
            for key in result:
                result[key].extend(study_method_resources.get(key, []))

        # Limit the number of results
        for key in result:
            if len(result[key]) > limit:
                result[key] = random.sample(result[key], limit)

        return result

    def _get_mental_health_resources(self):
        """Get mental health related resources"""
        # In a real project, resources should be searched by tag or keyword
        # Here we simplify by returning a few items from the database

        courses = self.resource_repo.search_online_courses_by_keyword("mental health")
        papers = self.resource_repo.search_papers_by_keyword("mental health")
        seminars = self.resource_repo.search_seminars_by_keyword("mental health")

        return {
            'online_courses': courses,
            'papers': papers,
            'seminars': seminars
        }

    def _get_study_method_resources(self):
        """Get study method related resources"""
        # In a real project, resources should be searched by tag or keyword

        courses = self.resource_repo.search_online_courses_by_keyword("study method")
        papers = self.resource_repo.search_papers_by_keyword("study method")
        seminars = self.resource_repo.search_seminars_by_keyword("study efficiency")

        return {
            'online_courses': courses,
            'papers': papers,
            'seminars': seminars
        }

    def _fill_popular_recommendations(self, recommendations, limit):
        """Fill recommendations with popular resources"""
        for key in recommendations:
            if len(recommendations[key]) < limit:
                needed = limit - len(recommendations[key])

                existing_ids = [item.id for item in recommendations[key]]

                popular_resources = []
                if key == 'online_courses':
                    popular_resources = self.resource_repo.get_popular_online_courses(needed * 2)
                elif key == 'papers':
                    popular_resources = self.resource_repo.get_popular_papers(needed * 2)
                elif key == 'seminars':
                    popular_resources = self.resource_repo.get_popular_seminars(needed * 2)

                for resource in popular_resources:
                    if resource.id not in existing_ids and len(recommendations[key]) < limit:
                        recommendations[key].append(resource)