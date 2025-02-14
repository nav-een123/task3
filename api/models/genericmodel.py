from typing import Union
from pydantic import BaseModel, Field, validator
from datetime import datetime,time

# task
class Task(BaseModel):
    name: str

class updatetask(BaseModel):
    name:str


# user
class createItems(BaseModel):
    name: str
    email:str
    phone_number: str

class updateItems(BaseModel):
    name: str
    email:str
    phone_number: str
   
# category
class createScheduleModel(BaseModel):
    date: str
    from_time:str
    to_time:str
    select_category: str = Field(..., description="The selected category")
    
class updateScheduleModel(BaseModel):
    date: str
    from_time:str
    to_time:str
    select_category: str = Field(..., description="The selected category")