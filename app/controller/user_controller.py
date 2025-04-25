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
        # 将 index 路由移到主路由
        self.bp.add_url_rule('/', 'index', self.index_page, methods=['GET'])
        
        # 页面路由
        self.bp.add_url_rule('/login', 'login_page', self.login_page, methods=['GET'])
        self.bp.add_url_rule('/profile', 'profile_page', self.profile_page, methods=['GET'])
        self.bp.add_url_rule('/logout', 'logout', self.logout, methods=['GET'])
        
        # API 路由
        self.bp.add_url_rule('/api/user/login', 'login', self.handle_login, methods=['POST'])
    
    def index_page(self):
        """首页"""
        return render_template('index.html')
    
    def login_page(self):
        """登录页面"""
        if request.cookies.get('access_token_cookie'):
            return redirect(url_for('auth.profile_page'))
        return render_template('user/login.html')
    
    @jwt_required()
    def profile_page(self):
        """用户资料页面"""
        user_id = int(get_jwt_identity())  # 将字符串ID转回整数
        user = self.user_repo.get_user_by_id(user_id)
        if not user:
            return redirect(url_for('auth.login_page'))
        return render_template('user/profile.html', user=user)
    
    def handle_login(self):
        """处理登录请求"""
        try:
            data = request.get_json()
            
            if not data or ('email' not in data and 'username' not in data) or 'password' not in data:
                return jsonify({
                    "message": "请提供用户名/邮箱和密码",
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
            
            # 创建响应
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
                # 设置JWT cookie
                set_access_cookies(response, auth_data['access_token'])
                print("Cookie设置成功")  # 添加调试信息
            except Exception as e:
                print(f"设置Cookie时出错: {str(e)}")  # 添加错误日志
                # 如果设置cookie失败，仍然返回token
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
            print(f"登录处理时出错: {str(e)}")  # 添加错误日志
            return jsonify({
                'success': False,
                'message': '服务器内部错误'
            }), 500
    
    def logout(self):
        """退出登录"""
        response = redirect(url_for('auth.login_page'))
        unset_jwt_cookies(response)
        flash('已成功退出登录', 'success')
        return response 