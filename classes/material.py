from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database.base import Base

class Material(Base):
    __tablename__ = "Materials"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    portal_id: Mapped[str] = mapped_column(String(20), unique=True)
    name: Mapped[str] = mapped_column(String(225))
    file_type: Mapped[str] = mapped_column(String(30))
    document_type: Mapped[str] = mapped_column(String(50))
    course_id: Mapped[int] = mapped_column(ForeignKey("Courses.id"))
