from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class Course(Base):
    def __init__(self, id, name, portal_url, semester_id):
        self.id = id
        self.name = name
        self.portal_url = portal_url
        self.semester_id = semester_id

    __tablename__ = "Courses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    portal_url: Mapped[str] = mapped_column(String(255), unique=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("Semesters.id"))
