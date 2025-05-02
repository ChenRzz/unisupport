from sqlalchemy.orm import Session, joinedload
from model.resource import Major, MajorResource, ResourceType, OnlineCourse, Paper, Seminar
from sqlalchemy import func

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


    def search_online_courses_by_keyword(self, keyword):
        """搜索关键词相关的在线课程"""
        return self.session.query(OnlineCourse).filter(
            OnlineCourse.name.like(f'%{keyword}%') |
            OnlineCourse.description.like(f'%{keyword}%')
        ).limit(10).all()

    def search_papers_by_keyword(self, keyword):
        """搜索关键词相关的论文"""
        return self.session.query(Paper).filter(
            Paper.title.like(f'%{keyword}%') |
            Paper.abstract.like(f'%{keyword}%') |
            Paper.keywords.like(f'%{keyword}%')
        ).limit(10).all()

    def search_seminars_by_keyword(self, keyword):
        """搜索关键词相关的研讨会"""
        return self.session.query(Seminar).filter(
            Seminar.title.like(f'%{keyword}%') |
            Seminar.description.like(f'%{keyword}%')
        ).limit(10).all()

    def get_popular_online_courses(self, limit=5):
        """获取热门在线课程"""
        # 在实际项目中，可以基于用户点击、评分等确定热门资源
        # 这里简化为随机选择一些课程
        return self.session.query(OnlineCourse).order_by(func.random()).limit(limit).all()

    def get_popular_papers(self, limit=5):
        """获取热门论文"""
        return self.session.query(Paper).order_by(func.random()).limit(limit).all()

    def get_popular_seminars(self, limit=5):
        """获取热门研讨会"""
        return self.session.query(Seminar).order_by(func.random()).limit(limit).all()