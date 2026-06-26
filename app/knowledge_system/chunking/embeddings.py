from ollama import embeddings

class EmbeddingEngine:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model

    async def embed(self, texts: list[str]) -> list[list[float]]:
        results = []
        for text in texts:
            result = embeddings(model=self.model, prompt=text)
            results.append(result["embedding"])
        return results