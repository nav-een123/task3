from fastapi.responses import JSONResponse
# from pydantic import BaseModel
from api.db.data import tasks
from api.models.model import Item
from fastapi import APIRouter,HTTPException
# from datetime import datetime
import uuid
# from fastapi import HTTPException
# from pymongo import MongoClient
from bson import ObjectId

router = APIRouter()
# class Item(BaseModel):
#     name: str
#     age:int
#     department:str
#     salary:float
#     due_date:datetime  
#     status: str = "New"  #ult value
#     uid: str = None  # Will be set dynamically



@router.post("/tasks")

def create_tasks(payload:Item):
    print(payload)

 # Assign values if they are missing
    if payload.uid is None:
        payload.uid = str(uuid.uuid4())

        print("After:", payload)
        task_data = payload.dict() 

    try:
        tasks.insert_one(task_data)
        return {"message": "Task created successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.get("/all")

def view_all_tasks(user_id: str):


    print("user_id----", user_id)
    
    try:
        user = tasks.find_one({"_id": ObjectId(user_id)})
        
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    print("user------", user)
    if user:
        user_id = str(user.get("_id"))
        return {"user_id": user_id, "name": user.get("name"), "age": user.get("age"),"department":user.get("department"),"salary":user.get("salary")}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    


@router.put("/{task_uid}")

def update_tasks(user_id: str, payload: Item):
    try:
        print("Updating user_id:", user_id)

        # Convert user_id to ObjectId
        object_id = ObjectId(user_id)

        # Remove None values from payload (so we only update provided fields)
        update_data = {k: v for k, v in payload.dict().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        # Perform the update operation
        result = tasks.update_one({"_id": object_id}, {"$set": update_data})

        # Check if a document was modified
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or no changes applied")

        return {"message": "User updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")
    

@router.delete("/{task_uid}")

def delete_tasks(task_uid:str):
    return None






