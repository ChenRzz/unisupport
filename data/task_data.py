from datetime import datetime, timedelta
from model.task import TaskType, TaskPriority, TaskStatus

def get_system_tasks(current_time):
    """Get predefined system tasks"""
    return [
        {
            "title": "Final Exam: Data Structures",
            "description": "Covers Chapters 1–12, including arrays, linked lists, trees, and graphs.",
            "due_date": current_time + timedelta(days=14),
            "priority": TaskPriority.HIGH,
            "type": TaskType.EXAM,
            "is_system_task": True,
            "course_name": "Data Structures and Algorithms",
            "external_url": "https://canvas.example.com/courses/ds/exams/final",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Project Report: Software Engineering",
            "description": "Submit Phase 1 project report, including requirement analysis and high-level design.",
            "due_date": current_time + timedelta(days=7),
            "priority": TaskPriority.HIGH,
            "type": TaskType.HOMEWORK,
            "is_system_task": True,
            "course_name": "Software Engineering",
            "external_url": "https://canvas.example.com/courses/se/assignments/report1",
            "created_at": current_time,
            "updated_at": current_time
        },
        {
            "title": "Assignment 3: Machine Learning",
            "description": "Complete the neural network programming assignment.",
            "due_date": current_time + timedelta(days=5),
            "priority": TaskPriority.MEDIUM,
            "type": TaskType.HOMEWORK,
            "is_system_task": True,
            "course_name": "Foundations of Machine Learning",
            "external_url": "https://canvas.example.com/courses/ml/assignments/hw3",
            "created_at": current_time,
            "updated_at": current_time
        }
    ]


def get_initial_user_tasks():
    """Initial task assignments for new users"""
    return {
        "student": {
            "tasks": [
                {
                    "task_index": 0,
                    "status": TaskStatus.TODO,
                    "notes": "Need to start reviewing."
                },
                {
                    "task_index": 1,
                    "status": TaskStatus.TODO,
                    "notes": "50% of requirement analysis completed."
                }
            ]
        },
        "student1": {
            "tasks": [
                {
                    "task_index": 0,
                    "status": TaskStatus.TODO,
                    "notes": "Start reviewing this week."
                },
                {
                    "task_index": 1,
                    "status": TaskStatus.TODO,
                    "notes": "Working on requirement analysis."
                }
            ]
        }
    }


def get_user_task_mappings():
    """Maps users to specific system tasks"""
    return {
        "student": {
            "tasks": [
                {
                    "task_index": 0,
                    "status": "todo",
                    "notes": "Need to review trees and graphs."
                },
                {
                    "task_index": 1,
                    "status": "in_progress",
                    "notes": "50% of requirement analysis completed."
                }
            ]
        },
        "student1": {
            "tasks": [
                {
                    "task_index": 1,
                    "status": "todo",
                    "notes": "Starting this week."
                },
                {
                    "task_index": 2,
                    "status": "in_progress",
                    "notes": "Learning neural networks."
                }
            ]
        }
    }
