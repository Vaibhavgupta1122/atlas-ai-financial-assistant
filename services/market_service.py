import yfinance as yf


class MarketService:

    @staticmethod
    def get_quote(symbol: str) -> dict:
        symbol = symbol.upper().strip()

        ticker = yf.Ticker(symbol)

        history = ticker.history(
            period="5d",
            interval="1d",
        )

        if history.empty:
            raise ValueError(
                f"No market data found for {symbol}."
            )

        latest = history.iloc[-1]

        current_price = float(latest["Close"])

        previous_close = None

        if len(history) >= 2:
            previous_close = float(
                history.iloc[-2]["Close"]
            )

        change = None
        change_percent = None

        if previous_close:
            change = current_price - previous_close

            change_percent = (
                (change / previous_close) * 100
            )

        return {
            "symbol": symbol,
            "price": round(current_price, 2),
            "previous_close": (
                round(previous_close, 2)
                if previous_close
                else None
            ),
            "change": (
                round(change, 2)
                if change is not None
                else None
            ),
            "change_percent": (
                round(change_percent, 2)
                if change_percent is not None
                else None
            ),
        }