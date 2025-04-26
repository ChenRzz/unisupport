from repo.taskRepo import TaskRepository
from model.task import Task, UserTask, TaskStatus, TaskType, TaskPriority
from datetime import datetime
from typing import List, Tuple, Dict, Any

class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def get_user_tasks(self, user_id: int) -> Dict[str, List[Dict[str, Any]]]:
        pass

    def create_custom_task(self, user_id: int, title: str, description: str, due_date: datetime, priority: str) -> Tuple[bool, str]:
        pass

    def update_task_status(self, user_task_id: int, status: str) -> Tuple[bool, str]:
        pass

    def update_task_notes(self, user_task_id: int, notes: str) -> Tuple[bool, str]:
        pass

    def delete_task(self, user_id: int, user_task_id: int) -> Tuple[bool, str]:
        pass

    def update_task(self, user_id: int, user_task_id: int, title: str, description: str, due_date: datetime, priority: str, notes: str) -> Tuple[bool, str]:
        pass
