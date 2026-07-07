import pandas as pd

from sqlalchemy import select

from app.database.db import engine, ohlcv_table


def load_ohlcv(
    symbol: str,
    timeframe: str,
    limit: int = 500,
) -> pd.DataFrame:

    query = (
        select(ohlcv_table)
        .where(
            ohlcv_table.c.symbol == symbol,
            ohlcv_table.c.timeframe == timeframe,
        )
        .order_by(
            ohlcv_table.c.timestamp.desc()
        )
        .limit(limit)
    )

    with engine.connect() as connection:
        result = connection.execute(query)

        rows = result.fetchall()

    df = pd.DataFrame(
        rows,
        columns=result.keys()
    )

    df = df.sort_values(
        "timestamp"
    )

    return df

def get_last_timestamp(
    symbol: str,
    timeframe: str,
):

    query = (
        select(ohlcv_table.c.timestamp)
        .where(
            ohlcv_table.c.symbol == symbol,
            ohlcv_table.c.timeframe == timeframe,
        )
        .order_by(
            ohlcv_table.c.timestamp.desc()
        )
        .limit(1)
    )

    with engine.connect() as connection:
        result = connection.execute(query).fetchone()

    if result:
        return result[0]

    return None   