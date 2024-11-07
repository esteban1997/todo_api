from fastapi import APIRouter,HTTPException,Depends,status
from models.todo import Todo
from models.user import User
from db.conection import db_dependency
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from schemas.todo_schemas import TodoBase
from typing import Annotated
from routers.authentication_bd import get_current_active_user
import re

router = APIRouter(
    prefix="/todo",
    tags=["todo"],
    responses={404: {"description": "Not found"}},
)  
  
@router.get("/todos")
def get_todo(db:db_dependency):
  todo = db.execute(select(Todo)).scalars().all()
  return todo

@router.get("/todos/{todo_id}")
def get_todo(todo_id: int, db:db_dependency):
  todo = db.execute(select(Todo).where(Todo.id == todo_id)).scalars().first()
  return todo
  
@router.post("/create_todo")
async def create_todo(todo : TodoBase,db:db_dependency,status_code=status.HTTP_201_CREATED):
  try:
    todo_element = Todo(description = todo.description,origin_task=todo.origin_task,user_id=todo.user_id,state_id = todo.state_id)
    db.add(todo_element)
    db.commit()
    db.refresh(todo_element)
  except IntegrityError as e:
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
  return todo_element

@router.get("/me/items/")
async def read_own_items(
  current_user: Annotated[User, Depends(get_current_active_user)],
  db: db_dependency
):
  todo = db.execute(select(Todo).where(Todo.user_id == current_user.id)).scalars().all()
  return [{"items": todo, "owner": current_user.username}]