
# UniSupport - University Student Support Platform

## Project Overview

**UniSupport** is a comprehensive platform designed to support university students by offering mental health assessments, academic resource recommendations, and study task management. It helps students manage their academic progress, understand their psychological status, and access quality learning materials relevant to their major.

## Key Features

### Mental Health Assessment
- Beck Depression Inventory (BDI-II)
- Study Status Assessment Questionnaire
- View history of assessment results
- Share assessment results anonymously

### Academic Resource Recommendation
- Major-based recommendations for courses, papers, and seminars
- Personalized recommendations based on mental health results
- Study method resources based on study status assessment
- Display of popular academic resources

### Task Management
- Create and track course assignments and exams
- Custom learning task creation
- Task status updates (To Do, In Progress, Completed)
- Task priority and deadline reminders

## Tech Stack

### Backend
- Python 3.8+
- Flask web framework
- SQLAlchemy ORM
- JWT for authentication
- SQLite (for development)

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap 5 framework
- Custom JavaScript components

## Installation Guide

### Requirements
- Python 3.8 or higher
- `pip` package manager
- `virtualenv` (recommended)

### Setup Steps

1. Clone the repository
```bash
git clone https://github.com/ChenRzz/unisupport.git
cd unisupport
```

2. Create and activate a virtual environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Linux/Mac
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the database
```bash
python model/init_db.py
```

5. Run the application
```bash
flask run
```

6. Access the app
```
http://localhost:5000
```

## Project Structure

```
unisupport/
├── app/                    # Main application module
│   ├── controllers/        # Route handlers (views)
│   └── templates/          # HTML templates
├── core/                   # Core business logic
├── data/                   # Initial data files
├── model/                  # Database models
├── repo/                   # Data access repositories
├── tests/                  # Unit tests
├── run.py                  # App entry point
└── requirements.txt        # Dependencies list
```

## Feature Modules

### User Authentication
- User registration and login
- JWT-based authentication
- User roles (student/admin)

### Questionnaire System
- Dynamically loaded questionnaires
- Auto scoring and result analysis
- Result storage and sharing

### Recommendation System
- Major-based resource categorization
- Personalized recommendation engine
- Resource search and filtering

### Task Management System
- Task creation and editing
- Status tracking and updates
- Deadline reminders

## User Guide

### For Students
1. Log in to the system
2. Complete mental health and study status questionnaires
3. View personalized resource recommendations
4. Browse major-related resources
5. Create and manage personal learning tasks

### For Admins
1. Log in with admin account
2. View anonymously shared assessment results
3. Manage system-wide resources and questionnaires

## Testing

Run all unit tests:
```bash
python tests/run_tests.py
```
