from typing import Annotated
from fastapi import Depends, FastAPI,HTTPException,status
from sqlmodel import Session
from pydantic import BaseModel
import models
from database import engine, SessionLocal
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager
import re
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
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the tables
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
#****************************************************************************************************
#declaracion de estructuras y endpoints

class TodoBase(BaseModel):
  description: str
  state_id : int
  
class TodoStateBase(BaseModel):
  description: str
  
@app.get("/todos")
def get_todo(db:db_dependency):
  todo = db.query(models.Todo).all()
  return todo

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, db:db_dependency):
  todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
  return todo

@app.get("/todos_states")
def get_todo(db:db_dependency):
  todo_states = db.query(models.TodoState).all()
  return todo_states
  
@app.post("/create_todo")
async def create_todo(todo : TodoBase,db:db_dependency):
  try:
    todo_element = models.Todo(description = todo.description,state_id = todo.state_id)
    db.add(todo_element)
    db.commit()
    db.refresh(todo_element)
  except IntegrityError as e:
    print("******************************************************")
    print(e.orig)
    print("******************************************************")
    error_message = str(e.orig)
    if re.search(r"la llave.*no está presente en la tabla", error_message, re.IGNORECASE):
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="El state_id proporcionado no existe en la tabla todo_state."
      )
    # Puedes manejar otros tipos de errores aquí si es necesario
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Ocurrió un error al crear el todo."
    )
    
@app.post("/create_todo_state")
async def create_todo_state(todo_state : TodoStateBase,db:db_dependency):
  print(todo_state)
  todo_state_element = models.TodoState(description=todo_state.description)
  db.add(todo_state_element)
  db.commit()
  db.refresh(todo_state_element)

