from pgvector.sqlalchemy import Vector
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.memory_system.short_term.models import Message

async def search_similar_messages(
    db: AsyncSession,
    query_embedding: list,
    user_id: int,
    limit: int = 3           
) -> list[Message]:
    
    result = await db.execute(
        select(Message)
        .where(Message.user_id == user_id)
        .order_by(Message.embedding.cosine_distance(query_embedding))
        .limit(limit)
    )
    return result.scalars().all()