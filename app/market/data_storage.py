import pandas as pd
from sqlalchemy.dialects.sqlite import insert
from app.core.logger import get_logger

from app.database.db import engine, ohlcv_table

logger = get_logger(__name__)


def save_ohlcv(
    df: pd.DataFrame,
    symbol: str,
    timeframe: str,
) -> None:

    records = []

    for _, row in df.iterrows():
        records.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "timestamp": row["timestamp"],
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
                "volume": row["volume"],
            }
        )

    with engine.begin() as connection:
        stmt = insert(ohlcv_table).values(records)

        stmt = stmt.on_conflict_do_nothing()

        connection.execute(stmt)

    #logger.info(f"OHLCV batch processed: {symbol} {timeframe}, rows={len(records)}")