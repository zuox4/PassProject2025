from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from pydantic import BaseModel
from database import Base


class ApcentModel(Base):
    __tablename__ = 'apcents'
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String(200))
    teacher_email = Column(String(200))
    datetime = Column(DateTime, default=datetime.now)
    class_name = Column(String(200))
    cause = Column(String(200))
