from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from model.db_base import Base
import enum
from datetime import datetime


class ResourceType(enum.Enum):
    ONLINE_COURSE = "online_course"
    PAPER = "paper"
    SEMINAR = "seminar"


# Major table
class Major(Base):
    __tablename__ = 'majors'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Name of the major
    description = Column(String(500))  # Description of the major
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


# Online course table
class OnlineCourse(Base):
    __tablename__ = 'online_courses'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)  # Course name
    description = Column(Text)  # Course description
    instructor = Column(String(100))  # Instructor
    duration = Column(String(50))  # Duration of the course
    url = Column(String(200))  # Course URL
    keywords = Column(String(200))  # Keywords
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Paper table
class Paper(Base):
    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # Title of the paper
    authors = Column(String(200))  # Authors
    publication = Column(String(200))  # Journal or conference
    publish_date = Column(DateTime)  # Date of publication
    abstract = Column(Text)  # Abstract
    keywords = Column(String(200))  # Keywords
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Seminar table
class Seminar(Base):
    __tablename__ = 'seminars'

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)  # Title of the seminar
    organizer = Column(String(100))  # Organizer
    date = Column(DateTime)  # Date of the event
    location = Column(String(200))  # Location
    description = Column(Text)  # Description
    keywords = Column(String(200))  # Keywords
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


# Major-resource association table
class MajorResource(Base):
    __tablename__ = 'major_resources'

    id = Column(Integer, primary_key=True)
    major_id = Column(Integer, ForeignKey('majors.id'), nullable=False)
    resource_type = Column(Enum(ResourceType), nullable=False)  # Type of resource
    resource_id = Column(Integer, nullable=False)  # Resource ID
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    major = relationship("Major")
