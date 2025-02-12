from fastapi import APIRouter,Request
from api.crud.crud import create_document,get_document_by_id,get_all_documents,update_document,delete_document

from api.models.genericmodel import createItems,createScheduleModel,updateItems,updateScheduleModel

from fastapi.templating import Jinja2Templates

from pathlib import Path



router = APIRouter()


# Get the absolute path to the templates folder

BASE_DIR = Path(__file__).resolve().parent.parent

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/")

def home(request: Request):

   return templates.TemplateResponse("sidebar.html", {"request": request})


@router.post("/{collection_name}")

async def create_item(collection_name: str, payload: createItems | createScheduleModel ):
    return create_document(collection_name, payload)



@router.get("/{collection_name}/{item_id}")

async def get_item(collection_name: str, item_id: str):
    return get_document_by_id(collection_name, item_id)



@router.get("/{collection_name}")

async def get_all_items(collection_name: str):
    return get_all_documents(collection_name)


@router.put("/{collection_name}/{item_id}")

async def update_item(collection_name: str, item_id: str, payload: updateItems | updateScheduleModel):
    return update_document(collection_name, item_id, payload)



@router.delete("/{collection_name}/{item_id}")

async def delete_item(collection_name: str, item_id: str):
    return delete_document(collection_name, item_id)

