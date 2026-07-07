from app.database import AsyncSessionLocal, engine, Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    """Create all tables and extentions"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)