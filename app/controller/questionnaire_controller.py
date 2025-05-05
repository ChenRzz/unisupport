from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.questionnaire import QuestionnaireService, QuestionnaireProcessor, QuestionnaireResultGenerator
from repo.questionnaireRepo import QuestionnaireRepository
from repo.userRepo import UserRepository
from model.db_base import session
from data.questionnaire_data import get_questionnaire_data
from datetime import datetime


class QuestionnaireController:
    bp = Blueprint('questionnaire', __name__,
                  template_folder='../templates',
                  static_folder='../static')

    def __init__(self):
        self.db_session = session
        self.questionnaire_repo = QuestionnaireRepository(session)
        self.user_repo = UserRepository(session)
        self.questionnaire_service = QuestionnaireService(self.questionnaire_repo)
        self.questionnaire_processor = QuestionnaireProcessor()
        self.register_routes()

    def register_routes(self):
        # Page routes
        self.bp.add_url_rule('/questionnaires', 'list_page', self.list_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/<int:questionnaire_id>', 'detail_page', self.detail_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/take/<questionnaire_type>', 'take_questionnaire', self.take_questionnaire, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/submit/<questionnaire_type>', 'submit_new_questionnaire', self.submit_new_questionnaire, methods=['POST'])
        self.bp.add_url_rule('/questionnaire/result', 'result_page', self.result_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/history', 'history_page', self.history_page, methods=['GET'])
        self.bp.add_url_rule('/questionnaire/shared', 'shared_page', self.shared_page, methods=['GET'])

        # API routes
        self.bp.add_url_rule('/api/questionnaires', 'list', self.list_questionnaires, methods=['GET'])
        self.bp.add_url_rule('/api/questionnaire/<int:questionnaire_id>/submit', 'submit', self.submit_questionnaire, methods=['POST'])
        self.bp.add_url_rule('/api/questionnaire/delete/<int:record_id>', 'delete_record',
                             self.delete_record, methods=['POST'])
        self.bp.add_url_rule('/api/questionnaire/calculate-result', 'calculate_result',
                             self.calculate_result, methods=['POST'])

    @jwt_required(optional=True)  # Allow access without login
    def list_page(self):
        """Questionnaire list page"""
        current_user = None
        try:
            user_id = get_jwt_identity()
            if user_id:
                current_user = self.user_repo.get_user_by_id(int(user_id))
        except:
            pass

        if not current_user:
            return redirect(url_for('auth.login_page'))

        if current_user.is_stuff:
            return redirect(url_for('questionnaire.shared_page'))

        questionnaires = []
        for q_type in self.questionnaire_processor.get_all_questionnaire_types():
            details = self.questionnaire_processor.get_questionnaire_details(q_type)
            if details:
                questionnaires.append({
                    'type': q_type,
                    'title': q_type.replace('_', ' ').title(),
                    'description': details.get('description', '')
                })

        return render_template('questionnaire/list_new.html', questionnaires=questionnaires)

    @jwt_required()
    def detail_page(self, questionnaire_id):
        """Questionnaire detail page"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            flash('Admins cannot take questionnaires', 'warning')
            return redirect(url_for('questionnaire.shared_page'))

        questionnaire = self.questionnaire_service.get_questionnaire(questionnaire_id)
        if not questionnaire:
            return "Questionnaire not found", 404
        return render_template('questionnaire/detail.html', questionnaire=questionnaire)

    @jwt_required()
    def take_questionnaire(self, questionnaire_type):
        """Take a new type of questionnaire"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            flash('Admins cannot take questionnaires', 'warning')
            return redirect(url_for('questionnaire.shared_page'))

        questionnaire = self.questionnaire_processor.get_questionnaire_details(questionnaire_type)
        if not questionnaire:
            flash('Questionnaire type not found', 'danger')
            return redirect(url_for('questionnaire.list_page'))

        return render_template('questionnaire/form_new.html', questionnaire=questionnaire)

    @jwt_required()
    def submit_new_questionnaire(self, questionnaire_type):
        """Submit a new type of questionnaire and calculate result"""
        user_id = int(get_jwt_identity())

        answers = {}
        for key, value in request.form.items():
            if key.startswith('question_'):
                question_id = int(key.replace('question_', ''))
                answers[question_id] = value

        is_shared = request.form.get('is_shared') == 'on'

        try:
            result = self.questionnaire_processor.calculate_score(questionnaire_type, answers)

            should_share = False
            if is_shared:
                total_score = result.get('total_score', 0)
                if questionnaire_type == 'beck_depression_inventory' and total_score >= 14:
                    should_share = True
                elif questionnaire_type == 'study_status_assessment' and total_score >= 40:
                    should_share = True

            result_content = QuestionnaireResultGenerator.generate_result_content(result)

            questionnaire_id = 0
            success, message = self.questionnaire_service.submit_questionnaire(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                answers=answers,
                is_shared=should_share,
                questionnaire_type=questionnaire_type
            )

            if not success:
                flash(f'Failed to save questionnaire record: {message}', 'danger')

            from flask import session
            session['questionnaire_result'] = result_content

            return redirect(url_for('questionnaire.result_page'))

        except Exception as e:
            flash(f'Failed to process questionnaire: {str(e)}', 'danger')
            return redirect(url_for('questionnaire.list_page'))

    @jwt_required()
    def result_page(self):
        """Display questionnaire result"""
        from flask import session

        result = session.get('questionnaire_result')
        if not result:
            flash('No result to display', 'warning')
            return redirect(url_for('questionnaire.list_page'))

        session.pop('questionnaire_result', None)

        return render_template('questionnaire/result.html', result=result)

    @jwt_required()
    def history_page(self):
        """User questionnaire history"""
        user_id = int(get_jwt_identity())
        questionnaires = self.questionnaire_service.get_user_questionnaires(user_id)
        return render_template('questionnaire/history.html', questionnaires=questionnaires)

    @jwt_required()
    def shared_page(self):
        """View shared questionnaire results (admins only)"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if not user.is_stuff:
            flash('Permission denied', 'danger')
            return redirect(url_for('questionnaire.list_page'))

        questionnaires = self.questionnaire_service.get_shared_questionnaires()
        return render_template('questionnaire/shared.html', questionnaires=questionnaires)

    @jwt_required()
    def list_questionnaires(self):
        """Get questionnaire list (API)"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)

        if user.is_stuff:
            return jsonify({
                'success': False,
                'message': 'Admins cannot take questionnaires'
            }), 403

        questionnaires_data = []

        for q_type in self.questionnaire_processor.get_all_questionnaire_types():
            details = self.questionnaire_processor.get_questionnaire_details(q_type)
            if details:
                questionnaires_data.append({
                    'id': 0,
                    'type': q_type,
                    'description': details.get('description', ''),
                    'created_at': datetime.now().isoformat(),
                    'is_new_type': True
                })

        old_questionnaires = self.questionnaire_service.get_questionnaires()
        for q in old_questionnaires:
            questionnaires_data.append({
                'id': q.id,
                'type': q.type,
                'description': q.description,
                'created_at': q.created_at.isoformat(),
                'is_new_type': False
            })

        return jsonify({
            'success': True,
            'data': questionnaires_data
        })

    @jwt_required()
    def submit_questionnaire(self, questionnaire_id):
        """Submit questionnaire answers (old API)"""
        user_id = int(get_jwt_identity())
        data = request.get_json()

        success, message = self.questionnaire_service.submit_questionnaire(
            user_id=user_id,
            questionnaire_id=questionnaire_id,
            answers=data['answers'],
            is_shared=data.get('is_shared', False)
        )

        return jsonify({
            'success': success,
            'message': message
        }), 200 if success else 500

    @jwt_required()
    def delete_record(self, record_id):
        """Delete questionnaire record"""
        user_id = int(get_jwt_identity())
        success, message = self.questionnaire_service.delete_questionnaire_record(record_id, user_id)

        return jsonify({
            'success': success,
            'message': message
        }), 200 if success else (404 if message == "Record not found" else 403)

    @jwt_required()
    def calculate_result(self):
        """Calculate questionnaire result API"""
        data = request.get_json()
        questionnaire_type = data.get('questionnaire_type')
        answers = data.get('answers', {})

        try:
            processed_answers = {}
            for question_id, answer in answers.items():
                q_id = int(question_id) if isinstance(question_id, str) else question_id
                if isinstance(answer, str) and answer.isdigit():
                    processed_answers[q_id] = int(answer)
                else:
                    processed_answers[q_id] = answer

            if questionnaire_type and processed_answers:
                if questionnaire_type in ['beck_depression_inventory', 'study_status_assessment']:
                    result = self.questionnaire_processor.calculate_score(questionnaire_type, processed_answers)
                    result_content = QuestionnaireResultGenerator.generate_result_content(result)

                    print(f"Calculated result: {result}")
                    print(f"Generated result content: {result_content}")

                    return jsonify({
                        'success': True,
                        'result': result_content
                    })
                else:
                    return jsonify({
                        'success': False,
                        'message': 'Result calculation for this questionnaire type is not supported'
                    })
            else:
                return jsonify({
                    'success': False,
                    'message': 'Missing parameters'
                })
        except Exception as e:
            import traceback
            print(f"Error in result calculation: {str(e)}")
            print(traceback.format_exc())

            return jsonify({
                'success': False,
                'message': f'Result calculation failed: {str(e)}'
            })