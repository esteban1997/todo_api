from pydantic import BaseModel

class TodoBase(BaseModel):
  description: str
  origin_task: int | None = None
  state_id : int