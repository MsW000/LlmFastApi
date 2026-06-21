from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from pgvector.sqlalchemy import Vector 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String)

    #один ко многим
    Message = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    embedding = Column(Vector(768)) #Это размер модели 768 nomic-embed-text