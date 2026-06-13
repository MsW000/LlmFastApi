from fastapi import FastAPI, Depends, HTTPException
from ollama import chat
from sqlalchemy.orm import Session

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

@app.get("/messages")
async def messages_depends(
    #пагинация
    limit: int = 10,
    offset: int = 0,
    sort: str = "desc",
    db: Session = Depends(get_db),
    ):

    query = db.query(Message)

    if sort == "desc":
        query = query.order_by(Message.id.desc())

    elif sort == "asc":
        query = query.order_by(Message.id.asc())
    
    messages = query.limit(limit).offset(offset).all()

    if sort not in ("asc", "desc"):
        raise HTTPException(
            status_code = 400,
            detail="sort must be 'asc' or 'desc'"
        )

    return messages

@app.get("/messages/{message_id}")
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    ):
    message = db.query(Message).filter(
        Message.id == message_id
        ).first()

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

@app.put("/messages/{message_id}")
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

    return {
        "id": message.id,
        "user_message": message.user_message,
        "ai_response": message.ai_response,
    }

@app.get(""
    "/messages/count", 
    response_model=MessageCount
)
async def count_message(
    db: Session = Depends(get_db)
    ):
    count = db.query(Message).count()

    return {
        "message_count": count
    }