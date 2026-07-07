import pandas as pd


class DataValidator:

    REQUIRED_COLUMNS = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
    ]


    def validate(self, df: pd.DataFrame) -> bool:

        if df.empty:
            raise ValueError(
                "Cannot validate empty dataframe"
            )

        self.check_columns(df)

        self.check_missing_values(df)

        self.check_price_logic(df)

        self.check_timestamp_order(df)

        return True


    def check_columns(self, df):

        missing = set(self.REQUIRED_COLUMNS) - set(df.columns)

        if missing:
            raise ValueError(
                f"Missing columns: {missing}"
            )


    def check_missing_values(self, df):

        if df.isnull().any().any():
            raise ValueError(
                "Data contains missing values"
            )


    def check_price_logic(self, df):

        invalid = df[
            (df["high"] < df["low"]) |
            (df["close"] > df["high"]) |
            (df["close"] < df["low"])
        ]

        if len(invalid) > 0:
            raise ValueError(
                "Invalid OHLC data detected"
            )


    def check_timestamp_order(self, df):

        if not df["timestamp"].is_monotonic_increasing:
            raise ValueError(
                "Timestamp order incorrect"
            )