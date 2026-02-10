from pydantic import BaseModel
from datetime import datetime
from typing import List


class DatasetCreate(BaseModel):
    name:str
    description:str



class DatasetRead(DatasetCreate):
    id:int
    created_at:datetime

    class Config:
        from_attributes=True

class DataElementCreate(BaseModel):
    name:str
    data_type:str
    dataset_id:int
    nullable:bool

class DataElementRead(DataElementCreate):
    id:int
    created_at:datetime

    class Config:
        from_attributes=True

class DS_DE(DatasetRead):
    elements:List[DataElementRead]=[]


class users_create(BaseModel):
    username:str
    password:str

