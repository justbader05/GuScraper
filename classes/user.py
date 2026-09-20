from __future__ import annotations
from typing import TYPE_CHECKING

from database.base import Base

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from classes.semester import Semester

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_email: Mapped[str] = mapped_column(String)
    email_password: Mapped[str] = mapped_column(String)
    semester_id: Mapped[int] = mapped_column(ForeignKey("Semesters.id")) 

    semester: Mapped[Semester] = relationship(
        back_populates="user"
    )