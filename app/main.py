from app.config.settings import settings
from app.database.db import init_db
from app.market.updater import MarketUpdater


def main() -> None:
    print("=" * 40)
    print(settings.app_name)
    print("=" * 40)

    init_db()
    print("Database initialized")

    updater = MarketUpdater()

    for symbol in settings.markets:
        for timeframe in settings.timeframes:
            updater.update(
                symbol=symbol,
                timeframe=timeframe,
            )


if __name__ == "__main__":
    main()