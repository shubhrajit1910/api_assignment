from fastapi import APIRouter,Depends,HTTPException,status,Path
from database import SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user
from schema import *
from models import *

router=APIRouter(tags=['Datasets'])

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[dict,Depends(get_current_user)]

@router.get("/list_datasets")
async def read_dataset(db:db_dependency):
    all_dataset=db.query(Dataset).all()
    return all_dataset

# @router.get("/read_all_datasets",response_model=list[DS_DE])
# async def read_all(db:db_dependency):
#     all_info=db.query(Dataset).all()
#     return all_info

@router.post("/add_dataset",status_code=status.HTTP_201_CREATED,response_model=DatasetRead)
async def new_dataset(db:db_dependency,dataset:DatasetCreate):
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

@router.put("/update_dataset/{dataset_id}")
async def update_dataset(user:user_dependency,db:db_dependency,user_req:DatasetCreate,dataset_id:int=Path(gt=0)):
    dataset=db.query(Dataset).filter(Dataset.id==dataset_id).first()

    if dataset is None:
        raise HTTPException(status_code=404,detail="dataset Not found")
    
    dataset.name=user_req.name
    dataset.description=user_req.description

    db.add(dataset)
    db.commit()
    db.refresh(dataset)
    return "Dataset updated"


@router.delete("/delete_dataset/{dataset_id}")
async def delete_dataset(user:user_dependency,db:db_dependency,dataset_id:int):
    DS=db.query(Dataset).filter(Dataset.id==dataset_id).first()
    if not DS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Dataset not found"
        )
    
    db.delete(DS)
    db.commit()
    