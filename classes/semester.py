from __future__ import annotations
from typing import TYPE_CHECKING

from database.base import Base
from datetime import date
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .course import Course
    from .user import User

class Semester(Base):
    __tablename__ = "Semesters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str] = mapped_column(String(10))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    directory: Mapped[str] = mapped_column(String)

    courses: Mapped[list["Course"]] = relationship(
        back_populates="semester",
        cascade="all, delete-orphan",
    )

    user: Mapped[User] = relationship(
        back_populates="semester"
    )
