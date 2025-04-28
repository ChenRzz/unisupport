from flask import Blueprint, render_template, jsonify, request, flash
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.task import TaskService
from repo.taskRepo import TaskRepository
from model.db_base import session
from datetime import datetime

class TaskController:
    bp = Blueprint('task', __name__,
                  template_folder='../templates',
                  static_folder='../static')
    
    def __init__(self):
        self.task_repo = TaskRepository(session)
        self.task_service = TaskService(self.task_repo)
        self.register_routes()
    
    def register_routes(self):
        self.bp.add_url_rule('/tasks', 'task_page', self.task_page, methods=['GET'])
        self.bp.add_url_rule('/api/tasks', 'list_tasks', self.list_tasks, methods=['GET'])
        self.bp.add_url_rule('/api/tasks', 'create_task', self.create_task, methods=['POST'])
        self.bp.add_url_rule('/api/tasks/<int:user_task_id>/status', 
                            'update_status', self.update_status, methods=['PUT'])
        self.bp.add_url_rule('/api/tasks/<int:user_task_id>/notes', 
                            'update_notes', self.update_notes, methods=['PUT'])
        self.bp.add_url_rule('/api/tasks/<int:user_task_id>', 
                            'delete_task', self.delete_task, methods=['DELETE'])
        self.bp.add_url_rule('/api/tasks/<int:user_task_id>', 
                            'update_task', self.update_task, methods=['PUT'])
    
    @jwt_required()
    def task_page(self):
        """任务管理页面"""
        return render_template('task/index.html')
    
    @jwt_required()
    def list_tasks(self):
        """获取用户的所有任务"""
        user_id = int(get_jwt_identity())
        tasks = self.task_service.get_user_tasks(user_id)
        return jsonify({
            'success': True,
            'data': tasks
        })
    
    @jwt_required()
    def create_task(self):
        """创建新任务"""
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        success, error = self.task_service.create_custom_task(
            user_id=user_id,
            title=data['title'],
            description=data.get('description', ''),
            due_date=datetime.fromisoformat(data['due_date']),
            priority=data['priority']
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        flash('任务创建成功', 'success')    
        return jsonify({
            'success': True,
            'message': '任务创建成功'
        })
    
    @jwt_required()
    def update_status(self, user_task_id):
        """更新任务状态"""
        data = request.get_json()
        success, error = self.task_service.update_task_status(
            user_task_id, data['status']
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400
            
        return jsonify({
            'success': True,
            'message': '状态更新成功'
        })
    
    @jwt_required()
    def update_notes(self, user_task_id):
        """更新任务笔记"""
        data = request.get_json()
        success, error = self.task_service.update_task_notes(
            user_task_id, data['notes']
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400
            
        return jsonify({
            'success': True,
            'message': '笔记更新成功'
        })
    
    @jwt_required()
    def delete_task(self, user_task_id):
        """删除任务"""
        user_id = int(get_jwt_identity())
        success, error = self.task_service.delete_task(user_id, user_task_id)
        
        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        flash('任务删除成功', 'success')
        return jsonify({
            'success': True,
            'message': '任务删除成功'
        })
    
    @jwt_required()
    def update_task(self, user_task_id):
        """更新任务"""
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        success, error = self.task_service.update_task(
            user_id=user_id,
            user_task_id=user_task_id,
            title=data['title'],
            description=data.get('description', ''),
            due_date=datetime.fromisoformat(data['due_date']),
            priority=data['priority'],
            notes=data.get('notes', '')
        )
        
        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400
        
        flash('任务更新成功', 'success')
        return jsonify({
            'success': True,
            'message': '任务更新成功'
        }) 