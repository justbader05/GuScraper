from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if TYPE_CHECKING:
    from classes.semester import Semester
    from classes.material import Material

class Course(Base):
    __tablename__ = "Courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    portal_url: Mapped[str] = mapped_column(String(255), unique=True)
    course_directory: Mapped[str] = mapped_column(String, nullable=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("Semesters.id", ondelete="CASCADE"))

    semester: Mapped[Semester] = relationship(
        back_populates="courses"
    )

    material: Mapped[list["Material"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
    )
