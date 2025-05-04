import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from core.task import TaskService
from model.task import Task, UserTask, TaskStatus, TaskType, TaskPriority


class TestTaskService(unittest.TestCase):
    def setUp(self):
        # Create mocked task repository
        self.task_repo_mock = MagicMock()

        # Create system task
        self.test_task = Task()
        self.test_task.id = 1
        self.test_task.title = "Final Exam for Data Structures"
        self.test_task.description = "Covers chapters 1–12, including arrays, linked lists, trees, and graphs."
        self.test_task.is_system_task = True
        self.test_task.type = TaskType.EXAM
        self.test_task.course_name = "Data Structures and Algorithms"
        self.test_task.priority = TaskPriority.HIGH

        # Create user task (linked to system task)
        self.test_user_task = UserTask()
        self.test_user_task.id = 1
        self.test_user_task.user_id = 1
        self.test_user_task.task_id = 1
        self.test_user_task.task = self.test_task
        self.test_user_task.status = TaskStatus.TODO
        self.test_user_task.notes = "Need to start preparing"

        # Create custom task
        self.custom_task = Task()
        self.custom_task.id = 2
        self.custom_task.title = "Custom Learning Task"
        self.custom_task.description = "Complete Java programming practice"
        self.custom_task.is_system_task = False
        self.custom_task.type = TaskType.CUSTOM
        self.custom_task.priority = TaskPriority.MEDIUM

        self.custom_user_task = UserTask()
        self.custom_user_task.id = 2
        self.custom_user_task.user_id = 1
        self.custom_user_task.task_id = 2
        self.custom_user_task.task = self.custom_task
        self.custom_user_task.status = TaskStatus.IN_PROGRESS

        # Mock repository behaviors
        self.task_repo_mock.get_user_task.return_value = self.test_user_task
        self.task_repo_mock.update_task.return_value = True

        # Create service instance
        self.task_service = TaskService(self.task_repo_mock)

    def test_create_custom_task_success(self):
        """Positive case: create custom task successfully"""
        self.task_repo_mock.create_task.return_value = self.test_task

        due_date = datetime.now() + timedelta(days=7)
        success, error = self.task_service.create_custom_task(
            user_id=1,
            title="New Task",
            description="Task description",
            due_date=due_date,
            priority="medium"
        )

        self.assertTrue(success)
        self.assertIsNone(error)
        self.assertEqual(self.task_repo_mock.create_task.call_count, 2)

    def test_update_task_status_success(self):
        """Positive case: successfully update task status"""
        self.task_repo_mock.update_user_task_status.return_value = True

        success, error = self.task_service.update_task_status(1, "completed")

        self.assertTrue(success)
        self.assertIsNone(error)
        self.task_repo_mock.update_user_task_status.assert_called_once_with(
            1, TaskStatus.COMPLETED
        )

    def test_update_task_status_failure(self):
        """Negative case: fail to update status due to missing task"""
        self.task_repo_mock.update_user_task_status.return_value = False

        success, error = self.task_service.update_task_status(999, "completed")

        self.assertFalse(success)
        self.assertEqual(error, "Task does not exist")

    def test_delete_task_success(self):
        """Positive case: successfully delete a custom task"""
        self.task_repo_mock.get_user_task.return_value = self.custom_user_task

        success, error = self.task_service.delete_task(1, 2)

        self.assertTrue(success)
        self.assertIsNone(error)
        self.task_repo_mock.delete_user_task.assert_called_once_with(2)

    def test_update_task_success(self):
        """Positive case: successfully update a custom task"""
        self.task_repo_mock.get_user_task.return_value = self.custom_user_task

        due_date = datetime.now() + timedelta(days=7)
        success, error = self.task_service.update_task(
            user_id=1,
            user_task_id=2,
            title="Updated Title",
            description="Updated Description",
            due_date=due_date,
            priority="high",
            notes="Updated notes"
        )

        self.assertTrue(success, f"Task update failed: {error}")
        self.assertIsNone(error)
        self.task_repo_mock.update_task.assert_called_once()

        self.assertEqual(self.custom_task.title, "Updated Title")
        self.assertEqual(self.custom_task.description, "Updated Description")
        self.assertEqual(self.custom_task.due_date, due_date)
        self.assertEqual(self.custom_task.priority, TaskPriority.HIGH)
        self.assertEqual(self.custom_user_task.notes, "Updated notes")


if __name__ == '__main__':
    unittest.main()
