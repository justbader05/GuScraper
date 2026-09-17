from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from ..database import base

class Course(base):
    __tablename__ = "Courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    portal_id: Mapped[str] = mapped_column(String(20), unique=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("Semesters.id"))