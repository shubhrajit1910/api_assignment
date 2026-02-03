from pydantic import BaseModel
from datetime import datetime
from typing import List


class DataElementCreate(BaseModel):
    name:str
    data_type:str
    dataset_id:int

class DataElementRead(DataElementCreate):
    id:int
    dataset_id:int
    created_at:datetime

    class Config:
        from_attributes=True



class DatasetCreate(BaseModel):
    name:str
    description:str


class DatasetRead(DatasetCreate):
    id:int
    created_at:datetime
    elements:List[DataElementRead]=[]

    class Config:
        from_attributes=True
