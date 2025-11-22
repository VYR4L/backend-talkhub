from models.user import User, UserCreate, UserUpdate
from typing import Optional
from datetime import datetime, timezone
from bson import ObjectId


class UserService:
    def __init__(self, collection):
        self.collection = collection

    def create_user(self, user_create: UserCreate) -> User:
        user_dict = user_create.model_dump()
        # Converte HttpUrl para string antes de salvar no MongoDB
        if "avatar_url" in user_dict and user_dict["avatar_url"]:
            user_dict["avatar_url"] = str(user_dict["avatar_url"])
        user_dict["created_at"] = datetime.now(timezone.utc)
        user_dict["updated_at"] = datetime.now(timezone.utc)
        result = self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        return User(**user_dict)

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        try:
            mongo_id = ObjectId(user_id)
        except Exception:
            return None
        user_data = self.collection.find_one({"_id": mongo_id})
        if user_data:
            user_data["_id"] = str(user_data["_id"])
            return User(**user_data)
        return None

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        try:
            mongo_id = ObjectId(user_id)
        except Exception:
            return None
        update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        if update_data:
            # Converte HttpUrl para string antes de salvar no MongoDB
            if "avatar_url" in update_data and update_data["avatar_url"]:
                update_data["avatar_url"] = str(update_data["avatar_url"])
            update_data["updated_at"] = datetime.now(timezone.utc)
            self.collection.update_one({"_id": mongo_id}, {"$set": update_data})
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id: str) -> bool:
        try:
            mongo_id = ObjectId(user_id)
        except Exception:
            return False
        result = self.collection.delete_one({"_id": mongo_id})
        return result.deleted_count > 0
