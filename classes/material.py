from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

if  TYPE_CHECKING:
    from classes.course import Course

class Material(Base):
    __tablename__ = "Materials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    moodle_id: Mapped[String] = mapped_column(String(20))
    portal_url: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(225))
    file_type: Mapped[str] = mapped_column(String(30))
    document_type: Mapped[str] = mapped_column(String(50))
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.id", ondelete="CASCADE"))

    course: Mapped["Course"] = relationship(
        back_populates="material"
    )

    def __init__(self, moodle_id, portal_url, name, course_id):
        self.moodle_id = moodle_id
        self.portal_url = portal_url
        self.name = name
        self.course_id = course_id
