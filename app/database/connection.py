
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./sales.db"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


def check_database():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        return True
