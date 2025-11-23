from services.chat_service import ChatService
from models.chat import ChatCreate, ChatUpdate, Chat
from typing import Optional


class ChatController:
    def __init__(self, collection):
        self.chat_service = ChatService(collection)

    def create_chat(self, chat_create: ChatCreate) -> Chat:
        return self.chat_service.create_chat(chat_create)
    
    def get_chat(self, chat_id: str) -> Optional[Chat]:
        return self.chat_service.get_chat_by_id(chat_id)        
    
    def update_chat(self, chat_id: str, chat_update: ChatUpdate) -> Optional[Chat]:
        return self.chat_service.update_chat(chat_id, chat_update)

    def delete_chat(self, chat_id: str) -> bool:
        return self.chat_service.delete_chat(chat_id)

    def list_chats(self) -> list[Chat]:
        return self.chat_service.list_chats()