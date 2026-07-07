from sqlalchemy import Column, Integer, Text, DateTime, JSON
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base

class EmbeddingModel(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    embedding = Column(Vector(768), nullable=False)
    metadata = Column(JSON, nullable=True)
    create_at = Column(DateTime, server_default=func.now())