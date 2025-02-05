from typing import Union
from pydantic import BaseModel

class Items(BaseModel):
    name: str
    email:str
    phone_number: str



