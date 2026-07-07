import asyncio
from app.knowledge_system.ingestion import Documentation

async def main():
    doc_ingestor = Documentation()

    count = await doc_ingestor.ingest_from_files("data/documents/")

    if count == 0:
        print("Test data..")
        test_text = """
        Jarvis - это AI ассистент для управления компьютером.
        Система использует Ollama для генерации ответов.
        Pgvector используется для хранения эмбеддингов.
        """
        await doc_ingestor.ingest(test_text, {"type": "test"})

if __name__ == "__main__":
    asyncio.run(main())