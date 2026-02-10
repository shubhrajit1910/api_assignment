from fastapi import APIRouter,Depends
from passlib.context import CryptContext
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from models import *
from schema import *
from fastapi.security import OAuth2PasswordRequestForm



router=APIRouter()

db_dependency=Annotated[Session,Depends(get_db)]

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

def authenticate_user(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hash_password):
        return False
    return True



@router.post("/auth",tags=["Auth"])
async def create_user(db:db_dependency,user_req:users_create):
    new_user=User(
        username=user_req.username,
        hash_password=bcrypt_context.hash(user_req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return new_user

@router.post("/tokens",tags=["Auth"])
async def login_for_access(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:db_dependency):
    val=authenticate_user(form_data.username,form_data.password,db)
    
    if not val:
        return "Authentication Failed"
    return "success"
