import ccxt
import pandas as pd
from app.config.settings import settings


class BinanceDataLoader:
    def __init__(self):
        self.exchange = ccxt.binance({
            "enableRateLimit": True,
        })

    def fetch_ohlcv(
        self,
        symbol,
        timeframe,
        limit=100,
        since=None,
    ) -> pd.DataFrame:

        if since:
            since = int(
                since.timestamp() * 1000
            ) + 1

        ohlcv = self.exchange.fetch_ohlcv(
            symbol,
            timeframe,
            limit=limit,
            since=since,
        )

        df = pd.DataFrame(
            ohlcv,
            columns=["timestamp", "open", "high", "low", "close", "volume"]
        )

        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

        return df