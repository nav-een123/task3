from fastapi import APIRouter,HTTPException,Request
from api.models.usermodel import Items
from api.db.data import users
from datetime import datetime
from bson import ObjectId
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import Response

router=APIRouter()


@router.get("/favicon.ico")
def favicon():
    return Response(status_code=204)  # No Content, prevents errors

BASE_DIR = Path(__file__).resolve().parent.parent # This gets the 'backend' directory

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))



@router.get("/")
def home(request: Request):
    return templates.TemplateResponse("sidebar.html", {
        "request": request,  # Required for Jinja in FastAPI
        # "title": "FastAPI Jinja Example",
        # "name": "Mantra Technologies",
        # "items": ["Developer", "Tester", "Accountant"],
        # "is_admin": False
    })

# @router.get("/createpopup")
# def home(request: Request):
#     return templates.TemplateResponse("createpopup.html", {
#         "request": request})


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