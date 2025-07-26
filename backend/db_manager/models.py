from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base
from datetime import datetime
from enum import Enum as PyEnum


Base = declarative_base()


class VacancyStatus(str, PyEnum):
    applied = "applied"
    interviewed = "interviewed"
    offered = "offered"
    rejected = "rejected"


class Resume(Base):
    __tablename__ = 'resumes'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)


class Vacancy(Base):
    __tablename__ = 'vacancies'
    id = Column(Integer, primary_key=True, index=True)
    link = Column(String, nullable=False)
    salary = Column(String)
    company = Column(String)
    position = Column(String)
    responded = Column(Boolean, default=True)  
    resume_id = Column(Integer, ForeignKey('resumes.id'), nullable=True)
    resume = relationship('Resume')
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(VacancyStatus), default=VacancyStatus.applied)
    basket = Column(String, nullable=True)
    rate = Column(Integer, nullable=True)
    score_match = Column(Float, nullable=True)
    score_best = Column(Float, nullable=True)
    contact1 = Column(String, nullable=True)
    contact2 = Column(String, nullable=True)
    comment = Column(String, nullable=True) 
    