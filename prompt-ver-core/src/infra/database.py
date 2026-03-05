from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


def build_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(db_url, echo=False, future=True)


def build_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(bind=engine, expire_on_commit=False, autobegin=True)


async def create_tables(engine: AsyncEngine) -> None:
    from src.adapters.persistence.orm_models import Base

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
