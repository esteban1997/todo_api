from pydantic import BaseModel

class TodoStateBase(BaseModel):
  description: str