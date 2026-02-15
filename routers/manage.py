from fastapi import APIRouter,Depends,HTTPException,status
from database import SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from schema import *
from models import *


router=APIRouter()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/list_datasets",tags=["Datasets"])
async def read_dataset(db:db_dependency):
    all_dataset=db.query(Dataset).all()
    return all_dataset

@router.get("/read_all_datasets",response_model=list[DS_DE],tags=["Datasets"])
async def read_all(db:db_dependency):
    all_info=db.query(Dataset).all()
    return all_info


@router.get("/list_data_element",tags=["Data Elements"])
async def read_element(db:db_dependency):
    all_data_element=db.query(DataElement).all()
    return all_data_element


@router.get("/read_specific_dataset/{id}",tags=["Datasets"])
async def read_specific_dataset(db:db_dependency,id:int):
    specific_data_element=db.query(DataElement).filter(DataElement.dataset_id==id).all()
    return specific_data_element


@router.post("/add_dataset",status_code=status.HTTP_201_CREATED,response_model=DatasetRead,tags=["Datasets"])
async def new_dataset(user:user_dependency,db:db_dependency,dataset:DatasetCreate):
    existing = db.query(Dataset).filter(Dataset.name == dataset.name).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Dataset name must be unique"
        )
    new_dataset=Dataset(**dataset.model_dump())
    db.add(new_dataset)
    db.commit()
    db.refresh(new_dataset)
    return new_dataset


@router.post("/add_dataelement",status_code=status.HTTP_201_CREATED,tags=["Data Elements"])
async def data_element(user:user_dependency,db:db_dependency,data_ele:DataElementCreate):
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


@router.delete("/delete_dataset/{dataset_id}",tags=["Datasets"])
async def delete_dataset(user:user_dependency,db:db_dependency,dataset_id:int):
    DS=db.query(Dataset).filter(Dataset.id==dataset_id).first()
    if not DS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    db.delete(DS)
    db.commit()
    












