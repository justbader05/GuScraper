from database.base import Base
from database.engine import engine
from scripts.scrape import scrape_files


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    scrape_files(1)
