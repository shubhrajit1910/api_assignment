import os
from dotenv import load_dotenv
from fastapi import APIRouter,Depends,HTTPException,status
from passlib.context import CryptContext
from database import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from models import *
from schema import *
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from datetime import timedelta,timezone



router=APIRouter(tags=['auth'])

db_dependency=Annotated[Session,Depends(get_db)]

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_bearer=OAuth2PasswordBearer(tokenUrl='tokens')

def authenticate_user(username:str,password:str,db):
    user=db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.hash_password):
        return False
    return user

def create_access_token(username:str,user_id:int,expires_delta:timedelta):
    encode={'sub':username,'id':user_id}
    expires=datetime.now(timezone.utc)+expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


async def get_current_user(token:Annotated[str,Depends(oauth2_bearer)]):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str=payload.get('sub')
        user_id:int=payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
        return {'username':username,'user_id':user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')



@router.post("/auth")
async def create_user(db:db_dependency,user_req:users_create):
    new_user=User(
        username=user_req.username,
        hash_password=bcrypt_context.hash(user_req.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # return new_user

@router.post("/tokens")
async def login_for_access(form_data:Annotated[OAuth2PasswordRequestForm,Depends()],
                           db:db_dependency):
    
    user=authenticate_user(form_data.username,form_data.password,db)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Could not validate user')
    
    token=create_access_token(user.username,user.id,timedelta(minutes=10))
    return {
        "access_token": token,
        "token_type": "bearer"
    }
