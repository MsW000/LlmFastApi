from pydantic import BaseModel
from pydantic_settings import BaseSettings

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

class MessageUpdate(BaseModel):
    user_message: str

class MessageCount(BaseModel):
    message_count: int

class MessageResponse(BaseModel):
    id: int
    user_message: str
    ai_response: str