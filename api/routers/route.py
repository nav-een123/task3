from fastapi import APIRouter,HTTPException
from api.models.usermodel import Items
from api.db.data import users
from datetime import datetime
from bson import ObjectId

router=APIRouter()

@router.post("/users")
def create_user(payload: Items):
    user_dict = payload.dict() 
    try:
        result=users.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get-user/{user_id}")
def get_user(user_id: str):  
    try:
        user = users.find_one({"_id": ObjectId(user_id)})    
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid user_id")
    if user:
        user_id = str(user.get("_id"))
        return {"user_id": user_id, "name": user.get("name"), "email": user.get("email")}
    else:
        raise HTTPException(status_code=404, detail="User not found")
    
@router.put("/update-user/{user_id}")
def update_user(user_id: str, payload: Items):
    try:
        # Convert user_id to ObjectId
        object_id = ObjectId(user_id)

        # Remove None values from payload (so we only update provided fields)
        update_data = {k: v for k, v in payload.dict().items() if v is not None}

        if not update_data:
            raise HTTPException(status_code=400, detail="No fields provided for update")

        # Perform the update operation
        result = users.update_one({"_id": object_id}, {"$set": update_data})

        # Check if a document was modified
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="User not found or no changes applied")

        return {"message": "User updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error updating user: {str(e)}")
    
@router.delete("/delete-user/{user_id}")
def delete_user(user_id: str):
    try:
        # Convert user_id to ObjectId
        object_id = ObjectId(user_id)

        # Delete user from database
        result = users.delete_one({"_id": object_id})

        # Check if a document was deleted
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {"message": "User deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error deleting user: {str(e)}")
