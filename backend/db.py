import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

load_dotenv()

engine = create_engine(os.environ.get("SQLALCHEMY_DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
