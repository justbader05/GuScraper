from ..database import base
from datetime import date
from sqlalchemy import String, Integer, Date
from sqlalchemy.orm import Mapped, mapped_column

class Semester(base):
    __tablename__ = "Semesters"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    season: Mapped[str] = mapped_column(String(10))
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)