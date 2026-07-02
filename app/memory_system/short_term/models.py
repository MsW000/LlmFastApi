from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    embedding = Column(Vector(768))

    owner = relationship("User", back_populates="messages")