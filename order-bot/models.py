from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Signal(Base):
    __tablename__ = 'order_result'

    id = Column(Integer, primary_key=True)
    type = Column(String(10), nullable=False)
    symbol = Column(String(20), nullable=False)
    entry = Column(DECIMAL(18, 2), nullable=False)
    stop_loss = Column(DECIMAL(18, 2), nullable=False)
    take_profit = Column(DECIMAL(18, 2), nullable=False)
    open_price = Column(DECIMAL(18, 2), nullable=False)
    close_price = Column(DECIMAL(18, 2), nullable=False)
    realized_pnl = Column(DECIMAL(18, 2), nullable=False)
    timestamp = Column(Integer, nullable=False)


DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgresql:5432/dev"
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
