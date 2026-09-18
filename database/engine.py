from pathlib import Path
from sqlalchemy import create_engine, event
import sqlite3


DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parent / 'database.db'}"
engine = create_engine(DATABASE_URL)
   
@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()