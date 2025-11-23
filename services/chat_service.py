from models.chat import Chat, ChatCreate, ChatUpdate, ChatSummary
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId


class ChatService:
    def __init__(self, collection):
        self.collection = collection

    def create_chat(self, chat_create: ChatCreate) -> Chat:
        chat_dict = chat_create.model_dump()
        chat_dict["created_at"] = datetime.now(timezone.utc)
        chat_dict["updated_at"] = datetime.now(timezone.utc)
        result = self.collection.insert_one(chat_dict)
        chat_dict["_id"] = str(result.inserted_id)
        return Chat(**chat_dict)

    def get_chat_by_id(self, chat_id: str) -> Optional[Chat]:
        try:
            mongo_id = ObjectId(chat_id)
        except Exception:
            return None
        chat_data = self.collection.find_one({"_id": mongo_id})
        if chat_data:
            chat_data["_id"] = str(chat_data["_id"])
            return Chat(**chat_data)
        return None

    def update_chat(self, chat_id: str, chat_update: ChatUpdate) -> Optional[Chat]:
        try:
            mongo_id = ObjectId(chat_id)
        except Exception:
            return None
        update_data = {k: v for k, v in chat_update.model_dump().items() if v is not None}
        if update_data:
            update_data["updated_at"] = datetime.now(timezone.utc)
            self.collection.update_one({"_id": mongo_id}, {"$set": update_data})
        return self.get_chat_by_id(chat_id)

    def delete_chat(self, chat_id: str) -> bool:
        try:
            mongo_id = ObjectId(chat_id)
        except Exception:
            return False
        result = self.collection.delete_one({"_id": mongo_id})
        return result.deleted_count > 0

    def list_chats(self) -> list[Chat]:
        chats = []
        for chat_data in self.collection.find():
            chat_data["_id"] = str(chat_data["_id"])
            chats.append(Chat(**chat_data))
        return chats