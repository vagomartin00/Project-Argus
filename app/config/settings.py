from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Application
    app_name: str = "Project Argus"
    debug: bool = False

    # Database
    database_url: str

    # AI
    ollama_url: str
    ollama_model: str

    # Logging
    log_level: str = "INFO"

    # Market Data
    exchange_name: str = "binance"

    markets: list[str] = [
        "BTC/USDT",
        "ETH/USDT",
    ]

    timeframes: list[str] = [
        "1h",
        #"5m",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


settings = Settings()