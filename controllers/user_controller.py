from services.user_service import UserService
from models.user import UserCreate, UserUpdate, User
from typing import Optional


class UserController:
    def __init__(self, collection):
        self.user_service = UserService(collection)

    def create_user(self, user_create: UserCreate) -> User:
        return self.user_service.create_user(user_create)
    
    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_service.get_user_by_id(user_id)        
    
    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        return self.user_service.update_user(user_id, user_update)

    def delete_user(self, user_id: str) -> bool:
        return self.user_service.delete_user(user_id)
