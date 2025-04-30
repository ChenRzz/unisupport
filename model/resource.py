from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from model.db_base import Base
import enum


class ResourceType(enum.Enum):
    ONLINE_COURSE = "online_course"
    PAPER = "paper"
    SEMINAR = "seminar"


# 专业表
class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # 专业名称
    description = Column(String(500))  # 专业描述
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# 在线课程表（改名）
class OnlineCourse(Base):
    __tablename__ = 'online_courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # 课程名称
    description = Column(String(500))  # 课程描述
    instructor = Column(String(100))  # 授课教师
    duration = Column(String(50))  # 课程时长
    url = Column(String(200))  # 添加课程链接字段
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# 论文表
class Paper(Base):
    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # 论文标题
    authors = Column(String(200))  # 作者
    publication = Column(String(200))  # 发表期刊/会议
    publish_date = Column(DateTime)  # 发表日期
    abstract = Column(String(1000))  # 摘要
    keywords = Column(String(200))  # 关键词
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# 研讨会表
class Seminar(Base):
    __tablename__ = 'seminars'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # 研讨会标题
    organizer = Column(String(100))  # 组织者
    date = Column(DateTime)  # 举办日期
    location = Column(String(200))  # 地点
    description = Column(String(500))  # 描述
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# 专业资源关联表
class MajorResource(Base):
    __tablename__ = 'major_resources'

    id = Column(Integer, primary_key=True)
    major_id = Column(Integer, ForeignKey('majors.id'), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)  # 资源类型
    resource_id = Column(Integer, nullable=False)  # 资源ID
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    major = relationship("Major")