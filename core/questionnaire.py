from repo.questionnaireRepo import QuestionnaireRepository
from model.questionnaire import UserQuestionnaire
from data.questionnaire_data import get_questionnaire_data
from datetime import datetime


class QuestionnaireService:
    def __init__(self, questionnaire_repo: QuestionnaireRepository):
        self.questionnaire_repo = questionnaire_repo

    def get_questionnaires(self):
        """Get all questionnaires"""
        return self.questionnaire_repo.get_all_questionnaires()

    def get_questionnaire(self, questionnaire_id: int):
        """Get a single questionnaire"""
        return self.questionnaire_repo.get_questionnaire_by_id(questionnaire_id)

    def get_user_questionnaires(self, user_id: int):
        """Get user's questionnaire records"""
        return self.questionnaire_repo.get_user_questionnaires(user_id)

    def get_shared_questionnaires(self):
        """Get shared questionnaire records"""
        return self.questionnaire_repo.get_shared_questionnaires()

    def submit_questionnaire(self, user_id: int, questionnaire_id: int, answers: dict, is_shared: bool,
                             questionnaire_type: str = None):
        """Submit questionnaire"""
        try:
            # If questionnaire type is provided and id is 0, find or create the questionnaire
            if questionnaire_type and questionnaire_id == 0:
                questionnaire = self.questionnaire_repo.get_questionnaire_by_type(questionnaire_type)

                if not questionnaire:
                    from model.questionnaire import Questionnaire
                    from data.questionnaire_data import get_questionnaire_data
                    from datetime import datetime

                    questionnaires_data = get_questionnaire_data(datetime.now())
                    questionnaire_data = None

                    for q_data in questionnaires_data:
                        if q_data['type'] == questionnaire_type:
                            questionnaire_data = q_data
                            break

                    if questionnaire_data:
                        questionnaire = Questionnaire(
                            type=questionnaire_type,
                            description=questionnaire_data.get('description', ''),
                            content=questionnaire_data.get('content', {}),
                            created_at=datetime.now(),
                            updated_at=datetime.now()
                        )
                        self.questionnaire_repo.create_questionnaire(questionnaire)
                        questionnaire_id = questionnaire.id
                else:
                    questionnaire_id = questionnaire.id

            if questionnaire_id <= 0:
                return False, "Invalid questionnaire ID"

            from model.questionnaire import UserQuestionnaire
            user_questionnaire = UserQuestionnaire(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                assessment=answers,
                is_shared=is_shared
            )

            self.questionnaire_repo.create_user_questionnaire(user_questionnaire)
            return True, "Submission successful"
        except Exception as e:
            return False, f"Submission failed: {str(e)}"

    def delete_questionnaire_record(self, record_id: int, user_id: int):
        """Delete questionnaire record"""
        try:
            record = self.questionnaire_repo.get_user_questionnaire_by_id(record_id)

            if not record:
                return False, "Record not found"

            if record.user_id != user_id:
                return False, "Unauthorized to delete this record"

            self.questionnaire_repo.delete_user_questionnaire(record)
            return True, "Deleted successfully"
        except Exception as e:
            return False, f"Deletion failed: {str(e)}"


class QuestionnaireProcessor:
    """Questionnaire processor: calculate score and generate result"""

    def __init__(self):
        self.questionnaires = get_questionnaire_data(datetime.now())
        self.questionnaire_map = {q["type"]: q for q in self.questionnaires}

    def _get_minimal_depression_advice(self):
        """Get minimal depression advice"""
        return [
            "Maintain a healthy lifestyle including regular schedule and moderate exercise",
            "Cultivate hobbies to add joy to life",
            "Stay socially active and keep in touch with friends and family",
            "Learn simple relaxation techniques like deep breathing and meditation"
        ]

    def _get_mild_depression_advice(self):
        """Get mild depression advice"""
        return [
            "Maintain regular routines and sufficient sleep",
            "Engage in at least 30 minutes of aerobic exercise daily",
            "Learn relaxation techniques like deep breathing and progressive muscle relaxation",
            "Avoid stimulants like alcohol and caffeine",
            "Share your feelings with friends and family",
            "Consider consulting the school mental health center"
        ]

    def _get_moderate_depression_advice(self):
        """Get moderate depression advice"""
        return [
            "Seek professional psychological counseling or therapy as soon as possible",
            "Maintain a regular daily routine, especially sleep",
            "Exercise regularly",
            "Talk to someone you trust about your concerns",
            "Learn cognitive skills to cope with negative thoughts",
            "Set small, achievable goals to reduce pressure",
            "Consider joining a school support group"
        ]

    def _get_severe_depression_advice(self):
        """Get severe depression advice"""
        return [
            "Strongly recommended to seek help from a professional psychiatrist or psychologist immediately",
            "Inform family, counselors, or trusted friends about your condition",
            "Do not bear it alone, seek help from support systems",
            "Follow advice from professionals",
            "Ensure you have companionship, avoid being alone for extended periods",
            "Seek campus psychological crisis intervention services",
            "Consider taking academic leave if necessary"
        ]

    def calculate_score(self, questionnaire_type, answers):
        """Calculate questionnaire score"""
        if questionnaire_type == 'beck_depression_inventory':
            total_score = 0
            for question_id, answer in answers.items():
                try:
                    answer_value = int(answer) if isinstance(answer, str) else answer
                    total_score += answer_value
                except (ValueError, TypeError):
                    print(f"Answer '{answer}' to question {question_id} could not be converted to integer")
                    continue

            if 0 <= total_score <= 13:
                level = "Minimal Depression"
                description = "Minimal or no depression"
                advice = self._get_minimal_depression_advice()
            elif 14 <= total_score <= 19:
                level = "Mild Depression"
                description = "Mild depression"
                advice = self._get_mild_depression_advice()
            elif 20 <= total_score <= 28:
                level = "Moderate Depression"
                description = "Moderate depression"
                advice = self._get_moderate_depression_advice()
            else:
                level = "Severe Depression"
                description = "Severe depression"
                advice = self._get_severe_depression_advice()

            return {
                "questionnaire_type": questionnaire_type,
                "total_score": total_score,
                "level": level,
                "description": description,
                "advice": advice
            }

        elif questionnaire_type == 'study_status_assessment':
            total_score = 0
            for question_id, answer in answers.items():
                try:
                    answer_value = int(answer) if isinstance(answer, str) else answer
                    total_score += answer_value
                except (ValueError, TypeError):
                    print(f"Answer '{answer}' to question {question_id} could not be converted to integer")
                    continue

            if 0 <= total_score <= 19:
                level = "Good"
                description = "Study status is good"
                detail = "You are managing your study tasks and time effectively."
                suggestions = [
                    "Keep up your current study habits",
                    "Try setting higher learning goals",
                    "Share your study strategies with others"
                ]
            elif 20 <= total_score <= 39:
                level = "Mild Fluctuation"
                description = "Mild fluctuations in study status"
                detail = "You can manage overall but sometimes feel difficulties or stress."
                suggestions = [
                    "Set more specific study plans",
                    "Improve time management skills",
                    "Take breaks regularly to avoid long periods of studying"
                ]
            elif 40 <= total_score <= 59:
                level = "Decline"
                description = "Noticeable decline in study status"
                detail = "Your study status is declining and may need adjustment and support."
                suggestions = [
                    "Reevaluate your goals and study methods",
                    "Seek help from peers or mentors",
                    "Pay attention to rest and well-being",
                    "Talk to your counselor about difficulties"
                ]
            else:
                level = "Severely Inefficient"
                description = "Study status is severely inefficient"
                detail = "Your study efficiency is very low and needs serious attention."
                suggestions = [
                    "Seek professional study guidance",
                    "Talk with a counselor or psychologist",
                    "Adjust your schedule and ensure enough sleep",
                    "Replan your study schedule and methods",
                    "Reduce workload temporarily and focus on recovery"
                ]

            return {
                "questionnaire_type": questionnaire_type,
                "total_score": total_score,
                "level": level,
                "description": description,
                "detail": detail,
                "suggestions": suggestions
            }

        else:
            raise ValueError(f"Unsupported questionnaire type: {questionnaire_type}")

    def get_questionnaire_details(self, questionnaire_type):
        """Get questionnaire details"""
        return self.questionnaire_map.get(questionnaire_type, None)

    def get_all_questionnaire_types(self):
        """Get all available questionnaire types"""
        return list(self.questionnaire_map.keys())


class QuestionnaireResultGenerator:
    """Generate result content for questionnaire"""

    @staticmethod
    def generate_result_content(result):
        """Generate result content"""
        questionnaire_type = result['questionnaire_type']

        if questionnaire_type == 'beck_depression_inventory':
            title = "BDI-II Assessment Result"
            score = result['total_score']
            level = result['level']
            description = result['description']
            advice_list = result['advice']

            content = f"""
            <div class="result-container">
                <div class="score-section">
                    <h3>Your Depression Score: {score}</h3>
                    <p>Result: <strong>{level}</strong> - {description}</p>
                </div>
                <div class="advice-section">
                    <h3>Recommended Actions:</h3>
                    <ul>
            """
            for advice in advice_list:
                content += f"<li>{advice}</li>\n"

            content += """
                    </ul>
                </div>
                <div class="disclaimer">
                    <p><strong>Important:</strong> This result is for reference only and does not replace a professional diagnosis. Please seek help if needed.</p>
                </div>
            </div>
            """

            return {
                "title": title,
                "content": content,
                "score": score,
                "level": level,
                "description": description,
                "advice": advice_list
            }

        elif questionnaire_type == 'study_status_assessment':
            level = result["level"]
            detail = result.get("detail", "")
            suggestions = result.get("suggestions", [])

            content = f"""
            <div class="result-container">
                <h2>Study Status Assessment Result</h2>
                <div class="score-section">
                    <p>Your Score: <strong>{result['total_score']}</strong></p>
                    <p>Result: <strong>{result['description']}</strong></p>
                </div>
                <div class="detail-section">
                    <p>{detail}</p>
                </div>
                <div class="advice-section">
                    <h3>Suggestions:</h3>
                    <ul>
            """
            for item in suggestions:
                content += f"<li>{item}</li>"

            content += """
                    </ul>
                </div>
                <div class="disclaimer">
                    <p>Note: This result is based on self-assessment and is for reference only. Please consult a counselor or mental health center if needed.</p>
                </div>
            </div>
            """

            return {
                "title": "Study Status Assessment Result",
                "content": content,
                "score": result['total_score'],
                "level": level,
                "description": result['description'],
                "detail": detail,
                "suggestions": suggestions
            }

        else:
            return {
                "title": "Questionnaire Result",
                "content": f"<p>Your score: {result['total_score']}</p><p>Level: {result['description']}</p>"
            }


def process_questionnaire_submission(questionnaire_type, answers):
    """
    Process questionnaire submission

    Args:
        questionnaire_type: Type of questionnaire
        answers: User answers

    Returns:
        dict: Result page content
    """
    processor = QuestionnaireProcessor()
    result = processor.calculate_score(questionnaire_type, answers)

    result_generator = QuestionnaireResultGenerator()
    return result_generator.generate_result_content(result)