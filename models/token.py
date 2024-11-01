from db.conection import Base
from models.user import User
from pydantic import BaseModel

class Token(BaseModel):  
  access_token: str
  token_type: str
  
class TokenData(BaseModel):  
  username: str | None = None

class UserInDB(BaseModel):
  hashed_password: str