from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
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
        """Task management page"""
        return render_template('task/index.html')

    @jwt_required()
    def list_tasks(self):
        """Get all tasks for the user"""
        user_id = int(get_jwt_identity())
        tasks = self.task_service.get_user_tasks(user_id)
        return jsonify({
            'success': True,
            'data': tasks
        })

    @jwt_required()
    def create_task(self):
        """Create a new task"""
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

        flash('Task created successfully', 'success')
        return jsonify({
            'success': True,
            'message': 'Task created successfully'
        })

    @jwt_required()
    def update_status(self, user_task_id):
        """Update task status"""
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
            'message': 'Status updated successfully'
        })

    @jwt_required()
    def update_notes(self, user_task_id):
        """Update task notes"""
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
            'message': 'Notes updated successfully'
        })

    @jwt_required()
    def delete_task(self, user_task_id):
        """Delete a task"""
        user_id = int(get_jwt_identity())
        success, error = self.task_service.delete_task(user_id, user_task_id)

        if not success:
            return jsonify({
                'success': False,
                'message': error
            }), 400

        flash('Task deleted successfully', 'success')
        return jsonify({
            'success': True,
            'message': 'Task deleted successfully'
        })

    @jwt_required()
    def update_task(self, user_task_id):
        """Update a task"""
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

        flash('Task updated successfully', 'success')
        return jsonify({
            'success': True,
            'message': 'Task updated successfully'
        })
    @jwt_required(optional=True)
    def task_page(self):
        """Task management page"""
        user_id = get_jwt_identity()

        if not user_id:
            return redirect(url_for('auth.login_page'))

        return render_template('task/index.html')