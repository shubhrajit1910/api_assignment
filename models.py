from database import Base
from sqlalchemy import Column,Integer,String,ForeignKey,DateTime,Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class Dataset(Base):
    __tablename__="datasets"

    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    name=Column(String,unique=True)
    description=Column(String)
    created_at=Column(DateTime,default=datetime.now)

    elements=relationship("DataElement",back_populates="dataset",cascade="all,delete")

class DataElement(Base):
    __tablename__="data_elements"

    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    dataset_id=Column(Integer,ForeignKey("datasets.id"),nullable=False)
    name=Column(String)
    data_type=Column(String)
    nullable=Column(Boolean,default=False)
    created_at=Column(DateTime,default=datetime.now)

    dataset=relationship("Dataset",back_populates="elements")


