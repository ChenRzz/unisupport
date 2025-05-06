from model import Base, engine, session, setup_relationships
from model.user import User
from model.questionnaire import Questionnaire
from model.resource import Paper, OnlineCourse, Seminar, Major, MajorResource, ResourceType
from werkzeug.security import generate_password_hash
import datetime

from data.user_data import get_users
from data.questionnaire_data import get_questionnaire_data
from data.resource_data import (
    get_online_courses, get_papers, get_seminars,
    get_majors, get_major_resource_mappings
)
from data.task_data import get_system_tasks, get_initial_user_tasks
from model.task import Task, UserTask

def init_db():
    print("Dropping all tables...")
    Base.metadata.drop_all(engine)

    print("Creating all tables...")
    Base.metadata.create_all(engine)

    # Ensure relationships are configured
    setup_relationships()

    db_session = session
    current_time = datetime.datetime.now(datetime.UTC)

    try:
        # Create majors
        print("Creating majors...")
        majors = {}
        for major_data in get_majors(current_time):
            major = Major(**major_data)
            db_session.add(major)
            majors[major_data["name"]] = major

        # Flush to get major IDs
        db_session.flush()

        # Create users and associate with majors
        print("Creating users...")
        for user_data in get_users(current_time):
            major_name = user_data.pop("major_name", None)  # Remove major field
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=generate_password_hash(user_data["password"]),
                is_stuff=user_data["is_stuff"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"]
            )

            if major_name and major_name in majors:
                user.major_id = majors[major_name].id

            db_session.add(user)

        # Create questionnaires
        print("Creating questionnaires...")
        for q_data in get_questionnaire_data(current_time):
            questionnaire = Questionnaire(**q_data)
            db_session.add(questionnaire)

        # Create resources
        print("Creating online courses...")
        courses = [OnlineCourse(**course_data)
                   for course_data in get_online_courses(current_time)]
        db_session.add_all(courses)

        print("Creating papers...")
        papers = [Paper(**paper_data)
                  for paper_data in get_papers(current_time)]
        db_session.add_all(papers)

        print("Creating seminars...")
        seminars = [Seminar(**seminar_data)
                    for seminar_data in get_seminars(current_time)]
        db_session.add_all(seminars)

        # Flush to get resource IDs
        db_session.flush()

        # Create major-resource mappings
        print("Creating major-resource mappings...")
        mappings = get_major_resource_mappings()
        for major_name, resources in mappings.items():
            major = majors[major_name]

            for course_idx in resources["online_courses"]:
                db_session.add(MajorResource(
                    major_id=major.id,
                    resource_type=ResourceType.ONLINE_COURSE,
                    resource_id=courses[course_idx].id,
                    created_at=current_time,
                    updated_at=current_time
                ))

            for paper_idx in resources["papers"]:
                db_session.add(MajorResource(
                    major_id=major.id,
                    resource_type=ResourceType.PAPER,
                    resource_id=papers[paper_idx].id,
                    created_at=current_time,
                    updated_at=current_time
                ))

            for seminar_idx in resources["seminars"]:
                db_session.add(MajorResource(
                    major_id=major.id,
                    resource_type=ResourceType.SEMINAR,
                    resource_id=seminars[seminar_idx].id,
                    created_at=current_time,
                    updated_at=current_time
                ))

        # Create system tasks
        print("Creating system tasks...")
        system_tasks = []
        for task_data in get_system_tasks(current_time):
            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                due_date=task_data["due_date"],
                priority=task_data["priority"],
                type=task_data["type"],
                is_system_task=task_data["is_system_task"],
                course_name=task_data["course_name"],
                external_url=task_data["external_url"],
                created_at=task_data["created_at"],
                updated_at=task_data["updated_at"]
            )
            db_session.add(task)
            system_tasks.append(task)

        # Flush to get task IDs
        db_session.flush()

        # Assign system tasks to users
        print("Assigning system tasks to users...")
        user_tasks_data = get_initial_user_tasks()
        for username, data in user_tasks_data.items():
            user = db_session.query(User).filter_by(username=username).first()
            if user:
                for task_info in data["tasks"]:
                    user_task = UserTask(
                        user_id=user.id,
                        task_id=system_tasks[task_info["task_index"]].id,
                        status=task_info["status"],
                        notes=task_info["notes"]
                    )
                    db_session.add(user_task)

        # Commit all changes
        db_session.commit()

        print("\nDatabase initialization complete!")
        print("\nAvailable accounts:")
        for user_data in get_users(current_time):
            print(f"\n{'Admin' if user_data['is_stuff'] else 'Student'} Account:")
            print(f"   Username: {user_data['username']}")
            print(f"   Email: {user_data['email']}")
            print(f"   Password: {user_data['password']}")

    except Exception as e:
        print(f"Error during database initialization: {str(e)}")
        db_session.rollback()
        raise

if __name__ == '__main__':
    init_db()
