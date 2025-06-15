from fastapi import APIRouter, Body
from datetime import datetime
from bson import ObjectId
from database import get_async_db  

router = APIRouter()

@router.post("/history")
async def store_chat_history(data: dict = Body(...)):
    db = get_async_db()
    collection = db["user_history"]

    user_id = data.get("user_id")
    chat_log = data.get("chat_log")  

    if not user_id or not chat_log:
        return {"success": False, "message": "Missing required fields"}

    entry = {
        "user_id": user_id,
        "chat_log": chat_log,
        "timestamp": datetime.utcnow()
    }

    result = await collection.insert_one(entry)
    return {"success": True, "id": str(result.inserted_id)}


@router.get("/history/{user_id}")
async def get_chat_history(user_id: str):
    db = get_async_db()
    collection = db["user_history"]

    cursor = collection.find({"user_id": user_id}).sort("timestamp", -1)
    history = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])
        history.append(doc)

    return {"success": True, "history": history}


@router.delete("/history/{entry_id}")
async def delete_chat_history(entry_id: str):
    db = get_async_db()
    collection = db["user_history"]

    result = await collection.delete_one({"_id": ObjectId(entry_id)})
    if result.deleted_count == 1:
        return {"success": True, "message": "Entry deleted"}
    return {"success": False, "message": "Entry not found"}
