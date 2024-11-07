from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    email: str 
    first_name: str 
    second_name: str | None = None
    first_lastname: str 
    second_lastname: str | None = None
    password : str