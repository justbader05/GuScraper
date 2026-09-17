from database.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "Users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    school_email: Mapped[str] = mapped_column(String)
    email_password: Mapped[str] = mapped_column(String)