from fastapi import  FastAPI
from db.conection import create_db_and_tables
from contextlib import asynccontextmanager
import routers.todo_routers 
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the tables
    create_db_and_tables()
    yield
    
app = FastAPI(lifespan=lifespan)
#****************************************************************************************************

app.include_router(routers.todo_routers.router)