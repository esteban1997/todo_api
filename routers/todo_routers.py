from fastapi import APIRouter,HTTPException,status
from pydantic import BaseModel
from models_test.todo import Todo
from db.conection import db_dependency
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
import re

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)  

class TodoBase(BaseModel):
  description: str
  origin_task: int | None = None
  state_id : int
  
@router.get("/todos")
def get_todo(db:db_dependency):
  todo = db.execute(select(Todo)).scalars().all()
  return todo

@router.get("/todos/{todo_id}")
def get_todo(todo_id: int, db:db_dependency):
  todo = db.execute(select(Todo).where(Todo.id == todo_id)).first()
  return todo
  
@router.post("/create_todo")
async def create_todo(todo : TodoBase,db:db_dependency):
  try:
    todo_element = Todo(description = todo.description,state_id = todo.state_id)
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
          detail="El estado seleccionado no existe entre las opciones."
      )
    # Puedes manejar otros tipos de errores aquí si es necesario
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Ocurrió un error al crear el todo."
    )