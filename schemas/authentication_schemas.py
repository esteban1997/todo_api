from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    username: str | None = None

class UserSchema(BaseModel):
    username: str
    email: str | None = None
    first_name: str | None = None
    second_name: str | None = None
    first_lastname: str | None = None
    second_lastname: str | None = None
    disabled: bool | None = None

class UserInDB(UserSchema):
  hashed_password: str