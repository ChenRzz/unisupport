from flask import Blueprint, render_template, jsonify, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.resource import ResourceService
from repo.resourceRepo import ResourceRepository
from repo.questionnaireRepo import QuestionnaireRepository
from repo.userRepo import UserRepository
from model.db_base import session

class ResourceController:
    bp = Blueprint('resource', __name__,
                  template_folder='../templates',
                  static_folder='../static')

    def __init__(self):
        self.resource_repo = ResourceRepository(session)
        self.user_repo = UserRepository(session)
        self.questionnaire_repo = QuestionnaireRepository(session)
        self.resource_service = ResourceService(self.resource_repo, self.questionnaire_repo)
        self.register_routes()

    def register_routes(self):
        self.bp.add_url_rule('/resources', 'resource_page', self.resource_page, methods=['GET'])
        self.bp.add_url_rule('/api/majors', 'list_majors', self.list_majors, methods=['GET'])
        self.bp.add_url_rule('/api/major/<int:major_id>/resources', 'get_major_resources',
                            self.get_major_resources, methods=['GET'])
        self.bp.add_url_rule('/api/resources/recommended', 'get_recommended_resources',
                           self.get_recommended_resources, methods=['GET'])

    @jwt_required(optional=True)
    def resource_page(self):
        """Resource recommendation page"""
        current_user = None
        try:
            user_id = get_jwt_identity()
            if user_id:
                current_user = self.user_repo.get_user_by_id(int(user_id))
        except:
            pass

        if not current_user:
            return redirect(url_for('auth.login_page'))

        majors = self.resource_service.get_all_majors()

        # Get personalized recommendations
        recommendations, error = self.resource_service.get_personalized_recommendations(current_user)

        return render_template('resource/index.html',
                              majors=majors,
                              user=current_user,
                              recommendations=recommendations)

    @jwt_required()
    def list_majors(self):
        """Get all majors"""
        majors = self.resource_service.get_all_majors()
        return jsonify({
            'success': True,
            'data': [{
                'id': m.id,
                'name': m.name,
                'description': m.description
            } for m in majors]
        })

    @jwt_required()
    def get_major_resources(self, major_id):
        """Get all resources for a major"""
        result, error = self.resource_service.get_major_resources(major_id)
        if error:
            return jsonify({
                'success': False,
                'message': error
            }), 404

        return jsonify({
            'success': True,
            'data': {
                'major': {
                    'id': result['major'].id,
                    'name': result['major'].name,
                    'description': result['major'].description
                },
                'resources': {
                    'online_courses': [{
                        'id': c.id,
                        'name': c.name,
                        'description': c.description,
                        'instructor': c.instructor,
                        'duration': c.duration,
                        'url': c.url
                    } for c in result['resources']['online_courses']],
                    'papers': [{
                        'id': p.id,
                        'title': p.title,
                        'authors': p.authors,
                        'publication': p.publication,
                        'publish_date': p.publish_date.isoformat() if p.publish_date else None,
                        'abstract': p.abstract,
                        'keywords': p.keywords
                    } for p in result['resources']['papers']],
                    'seminars': [{
                        'id': s.id,
                        'title': s.title,
                        'organizer': s.organizer,
                        'date': s.date.isoformat() if s.date else None,
                        'location': s.location,
                        'description': s.description
                    } for s in result['resources']['seminars']]
                }
            }
        })

    @jwt_required()
    def get_recommended_resources(self):
        """API to get personalized recommended resources"""
        try:
            user_id = get_jwt_identity()
            if not user_id:
                return jsonify({
                    'success': False,
                    'message': 'User not logged in'
                }), 401

            user = self.user_repo.get_user_by_id(int(user_id))
            if not user:
                return jsonify({
                    'success': False,
                    'message': 'User not found'
                }), 404

            recommendations, error = self.resource_service.get_personalized_recommendations(user)
            if error:
                return jsonify({
                    'success': False,
                    'message': error
                }), 500

            return jsonify({
                'success': True,
                'data': {
                    'online_courses': [{
                        'id': c.id,
                        'name': c.name,
                        'description': c.description,
                        'instructor': c.instructor,
                        'duration': c.duration,
                        'url': c.url
                    } for c in recommendations['online_courses']],
                    'papers': [{
                        'id': p.id,
                        'title': p.title,
                        'authors': p.authors,
                        'publication': p.publication,
                        'publish_date': p.publish_date.isoformat() if p.publish_date else None,
                        'abstract': p.abstract,
                        'keywords': p.keywords
                    } for p in recommendations['papers']],
                    'seminars': [{
                        'id': s.id,
                        'title': s.title,
                        'organizer': s.organizer,
                        'date': s.date.isoformat() if s.date else None,
                        'location': s.location,
                        'description': s.description
                    } for s in recommendations['seminars']]
                }
            })
        except Exception as e:
            return jsonify({
                'success': False,
                'message': f'Failed to get recommendations: {str(e)}'
            }), 500