from pathlib import Path

from database.base import Base
from database.engine import engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from scripts.scrape import scrape_files
from scripts.organize import organize_files
from classes.user import User
from terminalout import mainmenu

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    mainmenu(engine)




