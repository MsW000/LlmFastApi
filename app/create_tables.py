import asyncio
from sqlalchemy import text
from app.database import engine, Base

async def create_tables():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENTION IF NOT EXISTS vector"))
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())
    print("Tables created successfully")