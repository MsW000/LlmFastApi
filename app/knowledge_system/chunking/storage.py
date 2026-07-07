from sqlalchemy import text
from app.database import AsyncSessionLocal
#from app.knowledge_system.embeddings.schemas import EmbeddingModel

class VectorStorage:
    async def save(self, chunks: list[str], vector: list[list[float]], metadata: dict = None):
        """Save chunks and embeddings in Db"""
        async with AsyncSessionLocal() as session:
            for i, (chunks, vector) in enumerate(zip(chunks, vector)):
                await session.execute(
                    text("""
                        INSERT INTO embeddings (content, embedding, metadata) 
                        VALUES (:content, :embedding, :metadata)
                    """),
                    {
                        "content": chunk,
                        "embedding": vector,
                        "metadata": metadata or {}            
                    }
                )
                if (i+1) % 10 == 0:
                    print(f"Saved {i+1}/len(chunks)")
            await session.commit()
            print(f"Saved {len(chunks)} embeddings")

    async def search_similar(self, query_embedding: list[float], limit: int = 5):
        """Search similar from ORM"""
        from app.knowledge_system.embeddings.schemas import EmbeddingModel
        from sqlalchemy import select
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(
                    EmbeddingModel.content,
                    EmbeddingModel.metadata,
                    (1 - EmbeddingModel.embedding.op('<=>')(query_embedding)).label('similarity')
                )
                .order_by(EmbeddingModel.embedding.op('<=>')(query_embedding))
                .limit(limit)
            )

            return [
                {
                    "content": row[0],
                    "metadata": row[1],
                    "similarity": float[row[2]]
                }
                for row in result
            ]