from fastapi import APIRouter,Depends
from database import SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Annotated
from schema import *
from models import *
router=APIRouter()

db_dependency=Annotated[Session,Depends(get_db)]

@router.get("/read_dataset")
async def read_dataset(db:db_dependency):
    all_dataset=db.query(Dataset).all()
    return all_dataset

@router.get("/read_data_element")
async def read_element(db:db_dependency):
    all_data_element=db.query(DataElement).all()
    return all_data_element

@router.get("/read_data_element/{id}")
async def read_specific_dataset(db:db_dependency,id:int):
    specific_data_element=db.query(DataElement).filter(DataElement.dataset_id==id).all()
    return specific_data_element

@router.post("/add_dataset")
async def new_dataset(db:db_dependency,dataset:DatasetCreate):
    new_dataset=Dataset(**dataset.model_dump())
    db.add(new_dataset)
    db.commit()

@router.post("/add_dataelement")
async def data_element(db:db_dependency,data_ele:DataElementCreate):
    new_data_element=DataElement(**data_ele.model_dump())
    db.add(new_data_element)
    db.commit()










