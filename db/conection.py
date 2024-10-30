from sqlmodel import Session, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Creamos la URL de conexión
from dotenv import load_dotenv
import os
load_dotenv()

from typing import Annotated
from fastapi import Depends, FastAPI
from sqlmodel import Session
import models

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT",1234))
DB_NAME = os.getenv("DB_NAME")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()


#****************************************************************************************************
#creamos clases de atblas y tablas
def get_session():
    with Session(engine) as session:
        yield session
        
def create_db_and_tables():
    models.Base.metadata.create_all(engine)

SessionDep = Annotated[Session, Depends(get_session)]
#****************************************************************************************************
# conexion a base de datos
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()
    
db_dependency = Annotated[Session, Depends(get_db)]
#****************************************************************************************************