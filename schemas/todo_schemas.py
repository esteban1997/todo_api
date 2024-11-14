from pydantic import BaseModel

class TodoBase(BaseModel):
  description: str
  origin_task: int | None = None
  user_id: int | None = None
  state_id : int
  
class TodoUpdate(BaseModel):
  id:int
  state_id:int