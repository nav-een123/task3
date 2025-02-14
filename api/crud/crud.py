from api.db.data import users, category_collection,tasks
from bson import ObjectId
from fastapi import HTTPException
from pydantic import BaseModel



COLLECTIONS = {
    "task":tasks,
    "users": users,
    "categery": category_collection
}


def create_document(collection_name: str, payload: BaseModel):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")


    collection = COLLECTIONS[collection_name]
    document = payload.dict()


    if "start_time" in document:
        document["start_time"] = (document["start_time"])
    if "end_time" in document:
        document["end_time"] = (document["end_time"])


    try:
        result = collection.insert_one(document)
        document["_id"] = str(result.inserted_id)
        return {"message": f"{collection_name.capitalize()} created successfully", "data": document}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def get_document_by_id(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")


    collection = COLLECTIONS[collection_name]


    try:
        item = collection.find_one({"_id": ObjectId(item_id)})
        if not item:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")
        item["_id"] = str(item["_id"])
        return { "data": item}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




def get_all_documents(collection_name: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")


    collection = COLLECTIONS[collection_name]


    try:
        documents = list(collection.find({}))
        if not documents:
            raise HTTPException(status_code=404, detail=f"No {collection_name} found")
        for doc in documents:
            doc["_id"] = str(doc["_id"])
        return { "data": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




def update_document(collection_name: str, item_id: str, payload: BaseModel):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")


    collection = COLLECTIONS[collection_name]
    update_data = payload.dict(exclude_unset=True)


    try:
        update_result = collection.update_one({"_id": ObjectId(item_id)}, {"$set": update_data})


        if update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")


        return {"message": f"{collection_name.capitalize()} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



def delete_document(collection_name: str, item_id: str):
    if collection_name not in COLLECTIONS:
        raise HTTPException(status_code=400, detail="Invalid collection name")


    collection = COLLECTIONS[collection_name]


    try:
        result = collection.delete_one({"_id": ObjectId(item_id)})


        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail=f"{collection_name.capitalize()} not found")


        return {"message": f"{collection_name.capitalize()} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
