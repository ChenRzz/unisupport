# Empty file to make the app a Python package
from flask import Flask, request, make_response, redirect, url_for, flash
from flask_jwt_extended import JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTExtendedException
from datetime import timedelta
from core.login import LoginService
from repo.userRepo import UserRepository
from model.db_base import session

# Import base models
from model.user import User
from model.resource import Paper, OnlineCourse, Seminar, Major, MajorResource, ResourceType

# Temporarily comment out internal course imports until implemented
# from model.task import Assignment, UserAssignment

# Import questionnaire models
from model.questionnaire import Questionnaire, UserQuestionnaire

# Import controllers
from app.controllers.user_controller import UserController
from app.controllers.questionnaire_controller import QuestionnaireController
from app.controllers.resource_controller import ResourceController
from app.controllers.task_controller import TaskController

def create_app():
    app = Flask(__name__)

    # JWT Configuration
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = False  # Set to False for development
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for development
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
    app.config['JWT_COOKIE_SAMESITE'] = 'Lax'

    # Flask Configuration
    app.config['SECRET_KEY'] = 'your-flask-secret'

    # Initialize JWT
    jwt = JWTManager(app)

    # Inject current user into templates
    @app.context_processor
    def inject_user():
        try:
            if request.cookies.get('access_token_cookie'):
                verify_jwt_in_request()
                user_id = int(get_jwt_identity())
                user_repo = UserRepository(session)
                user = user_repo.get_user_by_id(user_id)
                return {'current_user': user}
        except JWTExtendedException:
            response = make_response(redirect(url_for('auth.login_page')))
            response.delete_cookie('access_token_cookie')
            flash('Session expired. Please log in again.', 'warning')
            return {'current_user': None}
        except Exception as e:
            print(f"Error retrieving user info: {str(e)}")
            return {'current_user': None}
        return {'current_user': None}

    # JWT Error Handling
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        response = make_response(redirect(url_for('auth.login_page')))
        response.delete_cookie('access_token_cookie')
        flash('Session expired. Please log in again.', 'warning')
        return response

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        response = make_response(redirect(url_for('auth.login_page')))
        response.delete_cookie('access_token_cookie')
        flash('Invalid session. Please log in again.', 'warning')
        return response

    # Create and register controllers
    db_session = session
    user_repo = UserRepository(db_session)
    login_service = LoginService(user_repo)
    user_controller = UserController(login_service, user_repo)
    questionnaire_controller = QuestionnaireController()
    resource_controller = ResourceController()
    task_controller = TaskController()

    # Register blueprints
    app.register_blueprint(user_controller.bp)
    app.register_blueprint(questionnaire_controller.bp)
    app.register_blueprint(resource_controller.bp)
    app.register_blueprint(task_controller.bp)

    return app
