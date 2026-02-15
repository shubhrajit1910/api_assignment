from fastapi import FastAPI
from database import engine
from models import Base 
from routers import dataelement,dataset,auth

app=FastAPI(
    title="Backend Data Management"
)

Base.metadata.create_all(bind=engine)
# app.include_router(manage.router)
app.include_router(dataset.router)
app.include_router(dataelement.router)
app.include_router(auth.router)


# @app.get("/")
# async def greet():
#     return "hi"