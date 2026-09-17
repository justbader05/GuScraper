from sqlalchemy import create_engine

def start_database():
    DATABASE_URL = "sqlite:///./database/database.db"
    engine = create_engine(DATABASE_URL)
    return engine