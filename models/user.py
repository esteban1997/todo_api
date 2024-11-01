from sqlalchemy import Column,Integer,String,Boolean
from db.conection import Base

class User(Base):
  __tablename__ = 'User'
  id = Column(Integer,primary_key=True,index=True, autoincrement=True)
  username = Column(String, nullable=False)
  email = Column(String, nullable=True)
  first_name = Column(String, nullable=False)
  second_name = Column(String, nullable=True)
  first_lastname = Column(String, nullable=False)
  second_lastname = Column(String, nullable=True)
  hashed_password = Column(String, nullable=False)
  disabled = Column(Boolean,default=False)