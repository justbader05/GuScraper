from __future__ import annotations
from typing import TYPE_CHECKING

from pathlib import Path

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
    file_path: Mapped[str] = mapped_column(String)
    file_type: Mapped[str] = mapped_column(String(30))
    document_type: Mapped[str] = mapped_column(String(50))
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.id", ondelete="CASCADE"))

    course: Mapped["Course"] = relationship(
        back_populates="material"
    )

    def detect_file_type(self):
        return Path(self.file_path).suffix.lstrip(".").lower()

    def detect_document_type(self):
        split_name = [word.lower() for word in self.name.split()]
        if self.file_type in ("pptx", "ppt"):
            return "Chapter"

        elif self.file_type in ("docx", "pdf"):
            if "syllabus" in split_name:
                return "Syllabus"
            else:
                return "Notes"

        else:
            return "Other"

    def __init__(self, moodle_id, portal_url, file_path, name, course_id):
        self.moodle_id = moodle_id
        self.portal_url = portal_url
        self.file_path = file_path
        self.name = name
        self.course_id = course_id
        self.file_type = self.detect_file_type()
        self.document_type = self.detect_document_type()