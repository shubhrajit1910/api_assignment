from fastapi import FastAPI
from database import engine
from models import Base 
from routers import manage

app=FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(manage.router)



# @app.get("/")
# async def greet():
#     return "hi"