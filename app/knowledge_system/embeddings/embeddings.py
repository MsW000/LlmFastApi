import asyncio
from typing import List
from ollama import AsyncClient
from langchain_community.embeddings import OllamaEmbeddings
from langchain_core.documents import Document

class EmbeddingEngine:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.client = AsyncClient()
        self.langchain_embeddings = OllamaEmbeddings(model=model)

    async def embed(self, texts: List[str]) -> List[List[float]]:
        """async generation embeddings for list and texts"""
        tasks = [self._embed_single(text) for text in texts]
        return await asyncio.gather(*tasks)
    
    async def _embed_single(self, text: str) -> List[float]:
        try:
            response = await self.client.embeddings(
                model=self.model,
                prompt=text
            )
            return response("embedding")
        except Exception as e:
            print(f"Wrong generation embeddings: {e}")
            raise

    async def embed_documents(self, documents: List[Document]) -> List[List[float]]:
        """Generation embeddings for documents LangChain"""
        texts = [doc.page_content for doc in documents]
        return await self.embed(texts)
    
    async def embed_query(self, query: str) -> List[float]:
        """Generation embeddings for query"""
        return await self._embed_single(query)