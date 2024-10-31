from fastapi import APIRouter
from pydantic import BaseModel
from models_test.todo_state import TodoState
from db.conection import db_dependency
from sqlalchemy.future import select

router = APIRouter(
    prefix="/todo_states",
    tags=["todo_states"],
    responses={404: {"description": "Not found"}},
)  
  
class TodoStateBase(BaseModel):
  description: str
  
@router.get("/todos_states")
def get_todo(db:db_dependency):
  todo_states = db.execute(select(TodoState)).scalars().all()
  return todo_states
    
@router.post("/create_todo_state")
async def create_todo_state(todo_state : TodoStateBase,db:db_dependency):
  print(todo_state)
  todo_state_element = TodoState(description=todo_state.description)
  db.add(todo_state_element)
  db.commit()
  db.refresh(todo_state_element)
