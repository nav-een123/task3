from typing import Union
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime,time


# task
class Task(BaseModel):
    name: str

class updatetask(BaseModel):
    name:str


# user
class createItems(BaseModel):
    name: str
    email:EmailStr
    contact:int
    password: str
    confirmPassword:str

class updateItems(BaseModel):
    name: str
    email:EmailStr
    contact:int
    password: str
    confirmPassword:str


class Login(BaseModel):
    email:EmailStr
    password:str


    
# category
class createScheduleModel(BaseModel):
    date: str
    from_time:str
    to_time:str
    select_category: str = Field(..., description="The selected category")
    task:str
    note:str
    
class updateScheduleModel(BaseModel):
    date: str
    from_time:str
    to_time:str
    select_category: str = Field(..., description="The selected category")
    task:str
    note:str