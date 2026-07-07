from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String,
    Float,
    DateTime,
    UniqueConstraint,
)

from app.config.settings import settings


engine = create_engine(
    settings.database_url,
    echo=False
)


metadata = MetaData()


ohlcv_table = Table(
    "ohlcv",
    metadata,

    Column("symbol", String, nullable=False),
    Column("timeframe", String, nullable=False),
    Column("timestamp", DateTime, nullable=False),

    Column("open", Float, nullable=False),
    Column("high", Float, nullable=False),
    Column("low", Float, nullable=False),
    Column("close", Float, nullable=False),
    Column("volume", Float, nullable=False),

    UniqueConstraint(
        "symbol",
        "timeframe",
        "timestamp",
        name="unique_candle"
    ),
)


def init_db():
    metadata.create_all(engine)