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
    print("正在删除所有表...")
    Base.metadata.drop_all(engine)

    print("正在创建所有表...")
    Base.metadata.create_all(engine)

    # 确保关系已设置
    setup_relationships()

    db_session = session
    current_time = datetime.datetime.now(datetime.UTC)

    try:
        # 先创建专业
        print("创建专业...")
        majors = {}
        for major_data in get_majors(current_time):
            major = Major(**major_data)
            db_session.add(major)
            majors[major_data["name"]] = major

        # 提交以获取专业ID
        db_session.flush()

        # 创建用户并关联专业
        print("创建用户...")
        for user_data in get_users(current_time):
            major_name = user_data.pop("major_name", None)  # 移除专业名称字段
            user = User(
                username=user_data["username"],
                email=user_data["email"],
                password_hash=generate_password_hash(user_data["password"]),
                is_stuff=user_data["is_stuff"],
                created_at=user_data["created_at"],
                updated_at=user_data["updated_at"]
            )

            # 如果指定了专业，设置关联
            if major_name and major_name in majors:
                user.major_id = majors[major_name].id

            db_session.add(user)

        # 创建问卷
        print("创建问卷...")
        for q_data in get_questionnaire_data(current_time):
            questionnaire = Questionnaire(**q_data)
            db_session.add(questionnaire)

        # 创建资源
        print("创建在线课程...")
        courses = [OnlineCourse(**course_data)
                   for course_data in get_online_courses(current_time)]
        db_session.add_all(courses)

        print("创建论文...")
        papers = [Paper(**paper_data)
                  for paper_data in get_papers(current_time)]
        db_session.add_all(papers)

        print("创建研讨会...")
        seminars = [Seminar(**seminar_data)
                    for seminar_data in get_seminars(current_time)]
        db_session.add_all(seminars)

        # 提交以获取ID
        db_session.flush()

        # 创建专业资源关联
        print("创建专业资源关联...")
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

        # 创建系统任务
        print("创建系统任务...")
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

        # 提交以获取任务ID
        db_session.flush()

        # 为用户分配系统任务
        print("分配系统任务给用户...")
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

        # 提交所有更改
        db_session.commit()

        print("\n数据库初始化完成！")
        print("\n可用账号:")
        for user_data in get_users(current_time):
            print(f"\n{'管理员' if user_data['is_stuff'] else '学生'}账号:")
            print(f"   用户名: {user_data['username']}")
            print(f"   邮箱: {user_data['email']}")
            print(f"   密码: {user_data['password']}")

    except Exception as e:
        print(f"初始化数据库时出错: {str(e)}")
        db_session.rollback()
        raise


if __name__ == '__main__':
    init_db()
