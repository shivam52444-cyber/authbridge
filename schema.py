from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, Float, Text, ForeignKey, DateTime
from databasesetup import Base
from datetime import datetime
from typing import Optional
from sqlalchemy import func


class User(Base):
    __tablename__ = "users"
    
    user_id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)
    dept_id: Mapped[int] = mapped_column(Integer)




class Job(Base):
    __tablename__ = "jobs"

    jobid: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text)
    department: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    reporting_to: Mapped[int] = mapped_column(Integer)
    posted_at = mapped_column(DateTime, server_default=func.now())


class Candidate(Base):
    __tablename__ = "candidates"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, default="unknown")
    resume_text: Mapped[str] = mapped_column(Text)
    
    job_id: Mapped[int] = mapped_column(ForeignKey("jobs.jobid"))
    
    score: Mapped[float] = mapped_column(Float)
    summary: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String,default="pending")
    hr_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    from typing import Optional

    hr_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)