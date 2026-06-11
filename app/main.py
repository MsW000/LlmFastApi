from fastapi import FastAPI, Depends
from ollama import chat
from sqlalchemy.orm import Session

from schemas import ChatRequest, ChatResponse
from models import Message
from db import get_db

app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
def chat_with_llm(
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