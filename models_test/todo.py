from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship,validates
from sqlalchemy.exc import IntegrityError
from db.conection import Base
  
class Todo(Base):
  __tablename__ = 'todo'

  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  description = Column(String, nullable=False)
  origin_task = Column(Integer, nullable=True)
  state_id = Column(Integer,ForeignKey("todo_state.id"))