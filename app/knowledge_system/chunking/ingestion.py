import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from .chunkink  import ChunkingEngine
from ..embeddings.embeddings import EmbeddingEngine
from .storage import VectorStorage

class Documentation:
    def __init__(self):
        self.chunker = ChunkingEngine()
        self.embedder = EmbeddingEngine()
        self.storage = VectorStorage()

    async def ingest(self, text: str, metadata: dict):
        chunks = self.chunker.split(text)                        # чанкинг
        vectors = await self.embedder.embed(chunks)              # эмбединги
        await self.storage.save(chunks, vectors, metadata or {}) #сохранение
        return len(chunks)
    
    async def ingest_from_files(self, source_path: str = "data/documents/"):
        all_chunks = []
        all_metadata = []

        if not os.path.exists(source_path):
            print(f"Path {source_path} not directory")
            return 0
        
        print("Load documents..")
        if os.path.isdir(source_path):
            loader = DirectoryLoader(source_path, glob="**/*.txt", loader_cls=TextLoader)
        else:
            loader = TextLoader(source_path)

        documents = loader.load()

        for doc in documents:
            chunks = self.chunker.split(doc.page_content)
            all_chunks.extend(chunks)
            #add metadata from file
            for _ in chunks:
                all_metadata.append({
                    "source": doc.metadata.get("source", "unknown"),
                    "file": os.path.basename(doc.metadata.get("source", "unknown"))
                })

        if all_chunks:
            print(f"Generated {len(all_chunks)} chunks")
            vectors = await self.embedder.embed(all_chunks)
            await self.storage.save(all_chunks, all_metadata)

        return len(all_chunks)
    
    async def search(self, query: str, limit: int = 5):
        """Search similar docs .."""
        query_embedding = await self.embedder.embed_query(query)
        return await self.storage.search_similar(query_embedding, limit)