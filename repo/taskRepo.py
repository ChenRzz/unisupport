from sqlalchemy.orm import Session
from model.task import Task, UserTask, TaskStatus
from typing import List, Optional

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_user_tasks(self, user_id: int) -> List[UserTask]:
        """Retrieve all tasks for a given user"""
        return self.session.query(UserTask).filter_by(user_id=user_id).all()

    def get_task(self, task_id: int) -> Optional[Task]:
        """Retrieve a single task by its ID"""
        return self.session.query(Task).get(task_id)

    def create_task(self, task: Task) -> Task:
        """Create a new task"""
        self.session.add(task)
        self.session.commit()
        return task

    def update_user_task_status(self, user_task_id: int, status: TaskStatus) -> bool:
        """Update the status of a user task"""
        user_task = self.session.query(UserTask).get(user_task_id)
        if user_task:
            user_task.status = status
            self.session.commit()
            return True
        return False

    def update_user_task_notes(self, user_task_id: int, notes: str) -> bool:
        """Update the notes of a user task"""
        user_task = self.session.query(UserTask).get(user_task_id)
        if user_task:
            user_task.notes = notes
            self.session.commit()
            return True
        return False

    def get_user_task(self, user_task_id: int) -> Optional[UserTask]:
        """Retrieve a user task by its ID"""
        return self.session.query(UserTask).get(user_task_id)

    def delete_user_task(self, user_task_id: int) -> None:
        """Delete a user task"""
        user_task = self.get_user_task(user_task_id)
        if user_task:
            self.session.delete(user_task)
            self.session.commit()

    def update_task(self, task: Task) -> None:
        """Update a task"""
        self.session.commit()
