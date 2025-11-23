from fastapi import Depends, APIRouter, HTTPException, status
from controllers.chat_controller import ChatController
from models.chat import ChatCreate, ChatUpdate, ChatOut, ChatListOut
from database.mongodb import MongoDB


router = APIRouter(prefix="/chats", tags=["chats"])


def get_chats_collection():
    """Dependency para obter a coleção de chats."""
    return MongoDB.get_collection("chats")


@router.post("/", response_model=ChatOut, status_code=status.HTTP_201_CREATED)
def create_chat(chat_create: ChatCreate, collection=Depends(get_chats_collection)):
    chat_controller = ChatController(collection)
    chat = chat_controller.create_chat(chat_create)
    return ChatOut(**chat.model_dump())


@router.get("/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: str, collection=Depends(get_chats_collection)):
    chat_controller = ChatController(collection)
    chat = chat_controller.get_chat(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatOut(**chat.model_dump())


@router.put("/{chat_id}", response_model=ChatOut)
def update_chat(chat_id: str, chat_update: ChatUpdate, collection=Depends(get_chats_collection)):
    chat_controller = ChatController(collection)
    chat = chat_controller.update_chat(chat_id, chat_update)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return ChatOut(**chat.model_dump())


@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_chat(chat_id: str, collection=Depends(get_chats_collection)):
    chat_controller = ChatController(collection)
    deleted = chat_controller.delete_chat(chat_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Chat not found")
    return None


@router.get("/", response_model=list[ChatOut])
def list_chats(collection=Depends(get_chats_collection)):
    chat_controller = ChatController(collection)
    chats = chat_controller.list_chats()
    return [ChatOut(**chat.model_dump()) for chat in chats]


