from pydantic import BaseModel
from typing import List, Optional

class ProductMention(BaseModel):
    message_text: Optional[str]
    channel_name: str

class ChannelActivity(BaseModel):
    date: str
    message_count: int

class VisualStat(BaseModel):
    image_category: str
    count: int

class MessageResponse(BaseModel):
    message_id: int
    message_text: Optional[str]
    views: Optional[int]