from typing import Union
from pydantic import BaseModel
from datetime import datetime

class Item(BaseModel):
    user_id:str
    name: str
    age:int
    department:str
    salary:float
    due_date:datetime  
    status: str = "New"  #ult value
    uid:str # Will be set dynamically