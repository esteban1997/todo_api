from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship
from db.conection import Base
  
class Todo(Base):
  __tablename__ = 'todo'

  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  description = Column(String, nullable=False)
  state_id = Column(Integer,ForeignKey("todo_state.id"))