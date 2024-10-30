from pydantic import BaseModel
from sqlalchemy import Column,Integer,String,ForeignKey
from database import Base

  
class Todo(Base):
  __tablename__ = 'todo'

  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  description = Column(String, nullable=False)
  state_id = Column(Integer,ForeignKey("todo_state.id"))
  
class TodoState(Base):
  __tablename__ = 'todo_state'
  
  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  description = Column(String,nullable=False)