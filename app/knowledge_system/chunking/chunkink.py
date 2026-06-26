from langchain_text_splitters import RecursiveCharacterTextSplitter

class ChunkingEngine:
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def split(self, text: str) -> list[str]:
        return self.splitter.split_text(text)