from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

# SQLite database URL. The `check_same_thread=False` is crucial for SQLite
# when used with FastAPI's asynchronous nature to prevent concurrency issues.
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create a SQLAlchemy engine
# echo=True will log all SQL statements, useful for debugging
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)


# Configure a sessionmaker to create new session objects
# autocommit=False: Changes won't be automatically committed
# autoflush=False: Changes won't be automatically flushed before a query
# expire_on_commit=False: Prevents objects from expiring after commit, useful for re-using objects
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()