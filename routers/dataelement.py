from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from schema import *
from models import *


router=APIRouter(tags=['DataElements'])

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]


@router.get("/list_data_element")
async def read_element(db:db_dependency):
    all_data_element=db.query(DataElement).all()
    return all_data_element


@router.get("/read_specific_dataset/{id}")
async def read_specific_dataset(db:db_dependency,id:int):
    specific_data_element=db.query(DataElement).filter(DataElement.dataset_id==id).all()
    return specific_data_element



@router.post("/add_dataelement",status_code=status.HTTP_201_CREATED)
async def data_element(db:db_dependency,data_ele:DataElementCreate):
    dataset = db.query(Dataset).filter(Dataset.id == data_ele.dataset_id).first()
    if not dataset:
        raise HTTPException(
            status_code=404,
            detail="Dataset not found"
        )
    existing=db.query(DataElement).filter(DataElement.name==data_ele.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Data element already exist"
        )
    new_data_element=DataElement(**data_ele.model_dump())
    db.add(new_data_element)
    db.commit()
    db.refresh(new_data_element)
    return new_data_element