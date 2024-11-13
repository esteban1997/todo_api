from typing import Annotated
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends,HTTPException,status,APIRouter
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm

from db.conection import db_dependency

from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError

from schemas.authentication_schemas import Token,TokenData,UserSchema
from schemas.user_schemas import CreateUser
from models.user import User

import jwt
from jwt.exceptions import InvalidTokenError

import os
from dotenv import load_dotenv
load_dotenv()

import re

#without prefix because i want to use it on the docs front provided by fastapi
router = APIRouter(
  prefix="",
  tags=["authentication"],
  responses={404: {"description": "Not found"}},
)  

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"),30)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
    
#para uso de jwt    
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#para uso de jwt
def verify_password(plain_password, hashed_password):
  return pwd_context.verify(plain_password, hashed_password)

#para uso de jwt
def get_password_hash(password):
  return pwd_context.hash(password)

def get_user(username: str, db:db_dependency):
  user = db.execute(select(User).where(User.username == username)).scalars().first()
  if user:
    return user

#para uso de jwt
def authenticate_user(username: str, password: str,db: db_dependency):
  user = get_user(username,db)
  if not user:
    return False
  if not verify_password(password, user.hashed_password):
    return False
  return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:db_dependency):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get("sub")
    if username is None:
      raise credentials_exception
    token_data = TokenData(username=username)
  except InvalidTokenError:
    raise credentials_exception
  user = get_user(username=token_data.username,db=db)
  if user is None:
    raise credentials_exception
  return user

async def get_current_active_user(
  current_user: Annotated[User, Depends(get_current_user)],
):
  if current_user.disabled:
    raise HTTPException(status_code=400, detail="Inactive user")
  return current_user

@router.post("/token")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: db_dependency
) -> Token:
  user = authenticate_user(form_data.username, form_data.password,db)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.username}, expires_delta=access_token_expires
  )
  return Token(access_token=access_token, token_type="bearer")


@router.post("/create_user")
async def create_user(
  user:CreateUser,
  db:db_dependency,
  status_code=status.HTTP_201_CREATED
):
  try:
    user_create = User(username = user.username,
    email = user.email ,
    first_name = user.first_name,
    second_name = user.second_name,
    first_lastname = user.first_lastname,
    second_lastname = user.second_lastname,
    hashed_password = pwd_context.hash(user.password))
    db.add(user_create)
    db.commit()
    db.refresh(user_create)
  except IntegrityError as e:
    error_message = str(e.orig)
    print(error_message)
    if re.search(r"llave duplicada viola restricción de unicidad «user_username_key»", error_message, re.IGNORECASE):
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="El nombre de usuario no se encuentra disponible."
      )
    # Puedes manejar otros tipos de errores aquí si es necesario
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Ocurrió un error al crear el todo."
    )
  return {"message" : "usuario creado correctamente"}

@router.get("/users/me", response_model=UserSchema)
async def read_users_me(
  current_user: Annotated[User, Depends(get_current_active_user)],
):
  return current_user