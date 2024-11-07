from sqlalchemy import Column,Integer,String
from db.conection import Base

class TodoState(Base):
  __tablename__ = 'todo_state'
  
  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  description = Column(String,nullable=False)
  