from fastapi import APIRouter,Request,HTTPException,Depends,Response
from api.crud.crud import create_document,get_document_by_id,get_all_documents,update_document,delete_document
from api.models.genericmodel import createItems,createScheduleModel,updateItems,updateScheduleModel,Task,updatetask,Login
from api.db.data import users, category_collection,tasks
from fastapi.templating import Jinja2Templates
from pathlib import Path
from api.utils.utils import verify_password,create_access_token,verify_access_token

router = APIRouter()

# Get the absolute path to the templates folder

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/")
def register(request: Request):
   return templates.TemplateResponse("register.html", {"request": request})

@router.get("/login")
def login(request: Request):
   return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(payload:Login,response:Response):
    user = users.find_one({"email":payload.email})
    if not user :
        raise HTTPException(status_code=400, detail="Invalid email or password")
    if not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    access_token = create_access_token(data={"email": user["email"]})
    fullname=user.get("name"," ")
    firstname=fullname.split()[0]
    response.set_cookie(
    
        key="access_token",
        value=access_token,
        httponly=True, 
        secure=True, 
        samesite="Lax",  
    )
    return {"access_token": access_token, "message": "Login successful", "firstname":firstname,"email": user["email"]}

@router.get("/protect")
async def protected_route(tokendata: dict = Depends(verify_access_token)):
    return {"message": "You are authenticated", "user": tokendata}

@router.get("/sidebar")
def home(request: Request):
   return templates.TemplateResponse("sidebar.html", {"request": request})

@router.get("/profile")
def login(request: Request):
   return templates.TemplateResponse("userprofile.html", {"request": request})

@router.post("/{collection_name}")
async def create_item(collection_name: str, payload: createItems | createScheduleModel | Task ):
    return create_document(collection_name, payload)

@router.get("/{collection_name}/{item_id}")
async def get_item(collection_name: str, item_id: str):
    return get_document_by_id(collection_name, item_id)

@router.get("/{collection_name}")
async def get_all_items(collection_name: str):
    return get_all_documents(collection_name)

@router.put("/{collection_name}/{item_id}")
async def update_item(collection_name: str, item_id: str, payload: updateItems | updateScheduleModel|updatetask):
    return update_document(collection_name, item_id, payload)

@router.delete("/{collection_name}/{item_id}")
async def delete_item(collection_name: str, item_id: str):
    return delete_document(collection_name, item_id)

