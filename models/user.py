from pydantic import BaseModel, Field, HttpUrl, ConfigDict, field_serializer
from typing import Optional
from bson import ObjectId
from datetime import datetime


class User(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    display_name: str
    public_key: str
    avatar_url: Optional[HttpUrl] = None
    created_at: datetime
    updated_at: datetime
    last_active_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('created_at', 'updated_at', 'last_active_at')
    def serialize_datetime(self, value: Optional[datetime]) -> Optional[str]:
        return value.isoformat() if value else None


class UserBase(BaseModel):
    display_name: str
    public_key: str
    avatar_url: Optional[HttpUrl] = None


class UserCreate(UserBase):
    phone_number: str
    phone_verified: bool = False  # TODO: implement phone verification logic


class UserUpdate(BaseModel):
    display_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None
    last_active_at: Optional[datetime] = None


class UserOut(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", serialization_alias="id")
    display_name: str
    public_key: str
    avatar_url: Optional[HttpUrl] = None
    created_at: datetime

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_serializer('created_at')
    def serialize_datetime(self, value: datetime) -> str:
        return value.isoformat()