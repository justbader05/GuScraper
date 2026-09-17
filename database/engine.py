from pathlib import Path

from sqlalchemy import create_engine


DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parent / 'database.db'}"
engine = create_engine(DATABASE_URL)
   
