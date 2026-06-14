from sqlalchemy import Column, Integer, Text
from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)