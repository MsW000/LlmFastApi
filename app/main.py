from fastapi import FastAPI, Depends, HTTPException, Query
from ollama import chat
from sqlalchemy.orm import Session
from sqlalchemy import or_

from schemas import ChatRequest, ChatResponse
from models import Message
from db import get_db

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