from pydantic import BaseModel

#чат 
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

#авторизация
class UserCreate(BaseModel):
    email: str
    password: str
    name: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str