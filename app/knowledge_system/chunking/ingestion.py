from .chunking  import ChunkingEngine
from .embeddings import EmbeddingEngine
from .storage import VectorStorage

class Documentation:
    def __init__(self):
        self.chunker = ChunkingEngine()
        self.embedder = EmbeddingEngine()
        self.storage = VectorStorage()

    async def ingest(self, text: str, metadata: dict):
        chunks = self.chunker.split(text)                  # чанкинг
        vectors = await self.embedder.embed(chunks)        # эмбединги
        await self.storage.save(chunks, vectors, metadata) #сохранение