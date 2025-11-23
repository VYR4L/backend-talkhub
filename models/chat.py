from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_serializer
from typing import Optional
from bson import ObjectId
from datetime import datetime


class Chat(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    type: str  # e.g., "private", "group"
    participant_ids: list[str]
    created_at: datetime
    updated_at: datetime
    last_message_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('created_at', 'updated_at', 'last_message_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.isoformat() if value else None
    

class BaseChat(BaseModel):
    type: str  # e.g., "private", "group"
    participant_ids: list[str]


class ChatCreate(BaseChat):
    pass


class ChatUpdate(BaseModel):
    type: Optional[str] = None
    participant_ids: Optional[list[str]] = None
    last_message_at: Optional[datetime] = None


class ChatOut(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", serialization_alias="id")
    type: str
    participant_ids: list[str]
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()
    

class ChatSummary(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", serialization_alias="id")
    type: str
    participant_ids: list[str]
    last_message_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('last_message_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.isoformat() if value else None
    

class ChatListOut(BaseModel):
    chats: list[ChatSummary]

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('chats')
    def serialize_chats(self, value: list[ChatSummary]) -> list[dict]:
        return [chat.model_dump() for chat in value]