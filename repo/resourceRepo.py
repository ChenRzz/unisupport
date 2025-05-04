from sqlalchemy.orm import Session, joinedload
from model.resource import Major, MajorResource, ResourceType, OnlineCourse, Paper, Seminar
from sqlalchemy import func


class ResourceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all_majors(self):
        """Retrieve all majors"""
        return self.session.query(Major).all()

    def get_major_by_id(self, major_id: int):
        """Retrieve a major by its ID"""
        return self.session.query(Major).get(major_id)

    def get_major_resources(self, major_id: int):
        """Retrieve all resources associated with a major"""
        return self.session.query(MajorResource).filter_by(major_id=major_id).all()

    def get_online_course(self, course_id: int):
        """Retrieve an online course by its ID"""
        return self.session.query(OnlineCourse).get(course_id)

    def get_paper(self, paper_id: int):
        """Retrieve a paper by its ID"""
        return self.session.query(Paper).get(paper_id)

    def get_seminar(self, seminar_id: int):
        """Retrieve a seminar by its ID"""
        return self.session.query(Seminar).get(seminar_id)

    def search_online_courses_by_keyword(self, keyword):
        """Search for online courses containing the keyword in name, description or keywords"""
        keyword = keyword.lower()
        return self.session.query(OnlineCourse).filter(
            OnlineCourse.name.ilike(f'%{keyword}%') |
            OnlineCourse.description.ilike(f'%{keyword}%') |
            OnlineCourse.keywords.ilike(f'%{keyword}%')
        ).limit(10).all()

    def search_papers_by_keyword(self, keyword):
        """Search for papers containing the keyword in title, abstract, or keywords"""
        keyword = keyword.lower()
        return self.session.query(Paper).filter(
            Paper.title.ilike(f'%{keyword}%') |
            Paper.abstract.ilike(f'%{keyword}%') |
            Paper.keywords.ilike(f'%{keyword}%')
        ).limit(10).all()

    def search_seminars_by_keyword(self, keyword):
        """Search for seminars containing the keyword in title, description or keywords"""
        keyword = keyword.lower()
        return self.session.query(Seminar).filter(
            Seminar.title.ilike(f'%{keyword}%') |
            Seminar.description.ilike(f'%{keyword}%') |
            Seminar.keywords.ilike(f'%{keyword}%')
        ).limit(10).all()

    def get_popular_online_courses(self, limit=5):
        """Retrieve popular online courses

        In a real-world application, popularity could be determined by views, ratings, etc.
        Here we simply return random courses as a placeholder.
        """
        return self.session.query(OnlineCourse).order_by(func.random()).limit(limit).all()

    def get_popular_papers(self, limit=5):
        """Retrieve popular papers (random selection)"""
        return self.session.query(Paper).order_by(func.random()).limit(limit).all()

    def get_popular_seminars(self, limit=5):
        """Retrieve popular seminars (random selection)"""
        return self.session.query(Seminar).order_by(func.random()).limit(limit).all()
