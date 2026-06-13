from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    answer: str

class MessageUpdate(BaseModel):
    user_message: str

class MessageCount(BaseModel):
    message_count: int