import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

engine = create_engine(os.environ.get("SQLALCHEMY_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Global variable to keep track of the query count
query_count = 0


# Event listener to count queries
def count_queries_before_cursor_execute(
    conn, cursor, statement, parameters, context, executemany
):
    global query_count
    query_count += 1


# Attach the event listener to the engine
event.listen(engine, "before_cursor_execute", count_queries_before_cursor_execute)


# Function to get the current query count
def print_query_count():
    print(query_count)


# Context manager to handle session and reset query count
class QueryCountSession:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def __enter__(self):
        self.db = self.session_factory()
        global query_count
        query_count = 0
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()
        global query_count
        query_count = 0


def get_session():
    with QueryCountSession(SessionLocal) as db:
        yield db


db_dependency = Annotated[Session, Depends(get_session)]


def save_db_model(db: db_dependency, obj_to_save):
    db.add(obj_to_save)
    db.commit()
    db.refresh(obj_to_save)


def update_db_model(db: db_dependency, obj_to_update):
    db.commit()
    db.refresh(obj_to_update)


def delete_db_model(db: db_dependency, obj_to_delete):
    db.delete(obj_to_delete)
    db.commit()
