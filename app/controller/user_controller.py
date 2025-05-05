from flask import Blueprint, jsonify, request, render_template, redirect, url_for, flash
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, set_access_cookies, unset_jwt_cookies, verify_jwt_in_request
from core.login import LoginService
from repo.userRepo import UserRepository

class UserController:
    bp = Blueprint('auth', __name__,
                  template_folder='../templates',
                  static_folder='../static')

    def __init__(self, login_service: LoginService, user_repo: UserRepository):
        self.login_service = login_service
        self.user_repo = user_repo
        self.register_routes()

    def register_routes(self):
        # Move index route to main
        self.bp.add_url_rule('/', 'index', self.index_page, methods=['GET'])

        # Page routes
        self.bp.add_url_rule('/login', 'login_page', self.login_page, methods=['GET'])
        self.bp.add_url_rule('/profile', 'profile_page', self.profile_page, methods=['GET'])
        self.bp.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])

        # API route
        self.bp.add_url_rule('/login', 'login', self.handle_login, methods=['POST'])

    def index_page(self):
        """Home page"""
        return render_template('index.html')

    def login_page(self):
        """Login page"""
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('auth.profile_page'))
        return render_template('user/login.html')

    @jwt_required()
    def profile_page(self):
        """User profile page"""
        user_id = int(get_jwt_identity())
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return redirect(url_for('auth.login_page'))
        return render_template('user/profile.html', user=user)

    def handle_login(self):
        """Handle login request"""
        try:
            data = request.get_json()

            if not data or ('email' not in data and 'username' not in data) or 'password' not in data:
                return jsonify({
                    "message": "Please provide username/email and password",
                    "success": False
                }), 400

            username_or_email = data.get('email') or data.get('username')
            password = data['password']

            success, message, auth_data = self.login_service.authenticate(username_or_email, password)

            if not success:
                return jsonify({
                    'success': False,
                    'message': message
                }), 422

            response = jsonify({
                'success': True,
                'message': message,
                'data': {
                    'token': auth_data['access_token'],
                    'user': {
                        'id': auth_data['user_id'],
                        'username': auth_data['username'],
                        'email': auth_data['email']
                    }
                }
            })

            try:
                set_access_cookies(response, auth_data['access_token'])
                print("Cookie set successfully")
            except Exception as e:
                print(f"Error setting cookie: {str(e)}")
                return jsonify({
                    'success': True,
                    'message': message,
                    'data': {
                        'token': auth_data['access_token'],
                        'user': {
                            'id': auth_data['user_id'],
                            'username': auth_data['username'],
                            'email': auth_data['email']
                        }
                    }
                })

            return response

        except Exception as e:
            print(f"Error handling login: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Internal server error'
            }), 500

    def logout(self):
        """Log out"""
        response = redirect(url_for('auth.login_page'))
        unset_jwt_cookies(response)
        flash('Logged out successfully', 'success')
        return response