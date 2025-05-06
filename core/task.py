from repo.taskRepo import TaskRepository
from model.task import Task, UserTask, TaskStatus, TaskType, TaskPriority
from datetime import datetime
from typing import List, Tuple, Dict, Any


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def get_user_tasks(self, user_id: int) -> Dict[str, List[Dict[str, Any]]]:
        """Get all tasks for the user, categorized by status"""
        user_tasks = self.task_repo.get_user_tasks(user_id)

        # Categorize tasks by status
        categorized_tasks = {
            'todo': [],
            'in_progress': [],
            'completed': []
        }

        for user_task in user_tasks:
            task_dict = {
                'id': user_task.task.id,
                'user_task_id': user_task.id,
                'title': user_task.task.title,
                'description': user_task.task.description,
                'due_date': user_task.task.due_date,
                'priority': user_task.task.priority.value,
                'type': user_task.task.type.value,
                'is_system_task': user_task.task.is_system_task,
                'course_name': user_task.task.course_name,
                'external_url': user_task.task.external_url,
                'notes': user_task.notes,
                'status': user_task.status.value
            }

            categorized_tasks[user_task.status.value].append(task_dict)

        return categorized_tasks

    def create_custom_task(self, user_id: int, title: str, description: str,
                           due_date: datetime, priority: str) -> Tuple[bool, str]:
        """Create a custom task"""
        try:
            # Create the task
            task = Task(
                title=title,
                description=description,
                due_date=due_date,
                priority=TaskPriority(priority),
                type=TaskType.CUSTOM,
                is_system_task=False
            )
            task = self.task_repo.create_task(task)

            # Create the user-task relation
            user_task = UserTask(
                user_id=user_id,
                task_id=task.id,
                status=TaskStatus.TODO
            )
            self.task_repo.create_task(user_task)

            return True, None
        except Exception as e:
            return False, str(e)

    def update_task_status(self, user_task_id: int, status: str) -> Tuple[bool, str]:
        """Update task status"""
        try:
            success = self.task_repo.update_user_task_status(
                user_task_id, TaskStatus(status)
            )
            if not success:
                return False, "Task not found"
            return True, None
        except Exception as e:
            return False, str(e)

    def update_task_notes(self, user_task_id: int, notes: str) -> Tuple[bool, str]:
        """Update task notes"""
        try:
            success = self.task_repo.update_user_task_notes(user_task_id, notes)
            if not success:
                return False, "Task not found"
            return True, None
        except Exception as e:
            return False, str(e)

    def delete_task(self, user_id: int, user_task_id: int) -> Tuple[bool, str]:
        """Delete a task"""
        try:
            user_task = self.task_repo.get_user_task(user_task_id)
            if not user_task:
                return False, "Task not found"

            if user_task.user_id != user_id:
                return False, "No permission to delete this task"

            if user_task.task.is_system_task:
                return False, "System tasks cannot be deleted"

            self.task_repo.delete_user_task(user_task_id)
            return True, None
        except Exception as e:
            return False, str(e)

    def update_task(self, user_id: int, user_task_id: int, title: str, description: str,
                    due_date: datetime, priority: str, notes: str) -> Tuple[bool, str]:
        """Update a task"""
        try:
            user_task = self.task_repo.get_user_task(user_task_id)
            if not user_task:
                return False, "Task not found"

            if user_task.user_id != user_id:
                return False, "No permission to update this task"

            if user_task.task.is_system_task:
                return False, "System tasks cannot be modified"

            # Update task information
            task = user_task.task
            task.title = title
            task.description = description
            task.due_date = due_date
            task.priority = TaskPriority(priority)
            user_task.notes = notes

            self.task_repo.update_task(task)
            return True, None
        except Exception as e:
            return False, str(e)