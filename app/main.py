from fastapi import FastAPI, Depends, HTTPException, Query
from ollama import chat
from sqlalchemy.orm import Session
from sqlalchemy import or_
from passlib.context import CryptContext
import hashlib
from jose import jwt 
from datetime import datetime, timedelta
import os
from app.auth import create_access_token, oauth2_scheme
from dotenv import load_dotenv
#from app.config import SECRET_KEY
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

load_dotenv()

from app.schemas import (
    ChatRequest,
    ChatResponse,
    MessageResponse,
    MessageUpdate,
    MessageCount,
    Token,
    UserResponse,
    UserCreate,
    UserLogin,
    Settings,
)

from app.models import Message, User
from app.db import get_db

#Временное решение
from app.database import Base, engine
from app.models import User

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/chat", response_model=ChatResponse)
async def chat_with_llm(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    response = chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": request.message,
            }
        ],
    )

    ai_answer = response["message"]["content"]

    message = Message(
        user_message=request.message,
        ai_response=ai_answer
    )

    db.add(message)
    db.commit()
    db.refresh(message)

    return ChatResponse(
        answer=ai_answer
    )

@app.get("/messages", response_model=list[MessageResponse])
async def get_messages(
    #пагинация
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = 0,
    #просто сорт и сессия
    search: str | None = None,
    sort: str = "desc",
    db: Session = Depends(get_db),
    ):

    query = db.query(Message)

    if sort not in ("asc", "desc"):
        raise HTTPException(
            status_code = 400,
            detail="sort must be 'asc' or 'desc'"
        )

    if search:
        query = query.filter(
            or_(
                Message.user_message.like(f"%{search}%"),
                Message.ai_response.like(f"%{search}%")
            )
        )

    if sort == "desc":
        query = query.order_by(Message.id.desc())

    elif sort == "asc":
        query = query.order_by(Message.id.asc())
    
    messages = query.limit(limit).offset(offset).all()

    return messages

@app.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    ):
    message = db.query(Message).filter(
        Message.id == message_id
        ).first()

    if message is None:
        raise HTTPException(
            status_code = 404,
            detail="Message not found"
        )
    return message

@app.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    ):
    message = db.query(Message).filter(
        Message.id == message_id
    ).first()

    if message is None:
        raise HTTPException(
            status_code = 404,
            detail="Message not found"
        )
    
    db.delete(message)
    db.commit()

    return {
        "message": "Deleted successfully"
    }

@app.put("/messages/{message_id}", response_model=MessageResponse)
async def put_message(
    message_id: int,
    request: MessageUpdate,
    db: Session = Depends(get_db),
    ):
    message = db.query(Message).filter(
        Message.id == message_id
    ).first()

    if message is None:
        raise HTTPException(
            status_code = 404,
            detail="Message not found"
        )
    
    message.user_message = request.user_message

    db.commit()
    db.refresh(message)

    return message

@app.get(""
    "/messages/count", 
    response_model=MessageCount
)
async def count_messages(
    db: Session = Depends(get_db)
    ):
    count = db.query(Message).count()

    return {
        "message_count": count
    }

#авторизация и ручки log reg

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
def hash_password(password:str) -> str:
    password = hashlib.sha256(password.encode()).hexdigest()
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password = hashlib.sha256(plain_password.encode()).hexdigest()
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/register")
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    
    existing_user = (
        db.query(User)
        .filter(User.email == user.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password),
        name=user.name
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created"
    }

@app.post("/login")
async def login_usr(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
    ):

    db_user = (
        db.query(User)
        .filter(User.email == form_data.username)
        .first()
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    if not verify_password(
        form_data.password, 
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401, 
            detail="Invalid credentials"
        )
    
    acess_token = create_access_token(
        {
            "sub": str(db_user.id) #Здесь id а не email/User может поменять email но не id ))
        }
    )

    return {
        "access_token": acess_token,
        "token_type": "bearer"
    }
#защищёнынй роут
#JWT
# 
#проверка подписи
# 
#получение пользователя
# 
#доступ к роуту. Тренимся делать уц-уц-уц. Если чё мне сложно и я устал (((
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
): 
    print("TOKEN RECEIVED:", token)
    try: 
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Ivalid token"
            )
        
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Ivalid token"
        )
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user 

@app.get("/me")
async def me(
    current_user: User = Depends(get_current_user)
):
    return{
        "id": current_user.id,
        "email": current_user.email,
        "name": current_user.name
    }