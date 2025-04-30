from sqlalchemy.orm import Session, joinedload
from model.resource import Major, MajorResource, ResourceType, OnlineCourse, Paper, Seminar


class ResourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_majors(self):
        """获取所有专业"""
        return self.session.query(Major).all()

    def get_major_by_id(self, major_id: int):
        """根据ID获取专业"""
        return self.session.query(Major).get(major_id)

    def get_major_resources(self, major_id: int):
        """获取专业的所有资源"""
        return self.session.query(MajorResource).filter_by(major_id=major_id).all()

    def get_online_course(self, course_id: int):
        """获取在线课程"""
        return self.session.query(OnlineCourse).get(course_id)

    def get_paper(self, paper_id: int):
        """获取论文"""
        return self.session.query(Paper).get(paper_id)

    def get_seminar(self, seminar_id: int):
        """获取研讨会"""
        return self.session.query(Seminar).get(seminar_id)