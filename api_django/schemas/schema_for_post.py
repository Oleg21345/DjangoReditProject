from fastapi import UploadFile
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class PostSchema(BaseModel):
    title: str = Field(..., max_length=255)
    content: Optional[str] = Field(default="Поки що тут нічого немає", max_length=1000)
    watched: Optional[int] = 0
    is_published: Optional[bool] = True
    category_id: int
    author_id: int

    model_config = ConfigDict(from_attributes=True)


class GroupMessageSchema(BaseModel):
    chat_group_id: int
    author_id: int
    body: Optional[str] = Field(default=None, max_length=300)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

class GroupMessageSchemaFile(BaseModel):
    chat_group_id: int
    author_id: int
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)



