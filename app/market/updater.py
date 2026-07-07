from app.market.data_loader import BinanceDataLoader
from app.market.data_storage import save_ohlcv
from app.database.repository import get_last_timestamp
from app.core.logger import get_logger
from app.market.data_validator import DataValidator


logger = get_logger(__name__)


class MarketUpdater:

    def __init__(self):
        self.loader = BinanceDataLoader()
        self.validator = DataValidator()

    def update(
        self,
        symbol: str,
        timeframe: str,
    ):
        logger.info(
            "-" * 60
        )

        logger.info(
            f"Updating {symbol} ({timeframe})"
        )

        logger.info(
            "-" * 60
        )

        last_timestamp = get_last_timestamp(
            symbol,
            timeframe,
        )

        logger.info(
            f"[{symbol} | {timeframe}] Latest stored candle in database: {last_timestamp}"
        )


        df = self.loader.fetch_ohlcv(
            symbol=symbol,
            timeframe=timeframe,
            limit=100,
            since=last_timestamp,
        )


        logger.info(
            f"[{symbol} | {timeframe}] Received {len(df)} candle(s) from exchange"
        )


        if last_timestamp:
            df = df[
                df["timestamp"] > last_timestamp
            ]


        logger.info(
            f"[{symbol} | {timeframe}] Found {len(df)} new candle(s)"
        )


        if df.empty:
            logger.info(
                "Update complete"
            )
            return


        self.validator.validate(df)

        logger.info(
            f"[{symbol} | {timeframe}] Saving {len(df)} new candle(s)"
        )


        save_ohlcv(
            df,
            symbol,
            timeframe,
        )


        logger.info(
            f"[{symbol} | {timeframe}] Latest saved candle: {df.iloc[-1]['timestamp']}"
        )


        logger.info(
            "Update complete"
        )