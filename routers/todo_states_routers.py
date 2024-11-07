from fastapi import APIRouter,status
from models.todo_state import TodoState
from db.conection import db_dependency
from sqlalchemy.future import select
from schemas.todo_state_schemas import TodoStateBase

router = APIRouter(
    prefix="/todo_states",
    tags=["todo_states"],
    responses={404: {"description": "Not found"}},
)    
  
@router.get("/todos_states")
def get_todo(db:db_dependency):
  todo_states = db.execute(select(TodoState)).scalars().all()
  return todo_states
    
@router.post("/create_todo_state")
async def create_todo_state(todo_state : TodoStateBase,db:db_dependency,status_code=status.HTTP_201_CREATED):
  print(todo_state)
  todo_state_element = TodoState(description=todo_state.description)
  db.add(todo_state_element)
  db.commit()
  db.refresh(todo_state_element)
  return todo_state_element
