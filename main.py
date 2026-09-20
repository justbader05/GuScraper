from pathlib import Path

from database.base import Base
from database.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from scripts.scrape import scrape_files
from scripts.organize import organize_files
from classes.user import User


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    with Session(engine) as e:
        user = e.get(User, 1)

    download_path = Path(user.obsidian_root)
    organize_files(scrape_files(1,download_path), download_path, engine) 
