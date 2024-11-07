from fastapi import  FastAPI
from db.conection import create_db_and_tables
from contextlib import asynccontextmanager
import routers.authentication_bd
import routers.todo_routers
import routers.todo_states_routers 
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the tables
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#****************************************************************************************************

app.include_router(routers.authentication_bd.router)
app.include_router(routers.todo_routers.router)
app.include_router(routers.todo_states_routers.router)
# app.include_router(routers.authentication_routers.router)