import re


class IntentService:

    # Common company → ticker mappings
    COMPANY_TICKERS = {
        "apple": ("Apple", "AAPL"),
        "aapl": ("Apple", "AAPL"),

        "microsoft": ("Microsoft", "MSFT"),
        "msft": ("Microsoft", "MSFT"),

        "nvidia": ("NVIDIA", "NVDA"),
        "nvda": ("NVIDIA", "NVDA"),

        "amazon": ("Amazon", "AMZN"),
        "amazon.com": ("Amazon", "AMZN"),
        "amzn": ("Amazon", "AMZN"),

        "google": ("Alphabet", "GOOGL"),
        "alphabet": ("Alphabet", "GOOGL"),
        "googl": ("Alphabet", "GOOGL"),
        "goog": ("Alphabet", "GOOG"),

        "tesla": ("Tesla", "TSLA"),
        "tsla": ("Tesla", "TSLA"),

        "meta": ("Meta Platforms", "META"),
        "facebook": ("Meta Platforms", "META"),
        "meta platforms": ("Meta Platforms", "META"),

        "netflix": ("Netflix", "NFLX"),
        "nflx": ("Netflix", "NFLX"),

        "amd": ("AMD", "AMD"),
        "advanced micro devices": (
            "Advanced Micro Devices",
            "AMD",
        ),

        "intel": ("Intel", "INTC"),
        "intc": ("Intel", "INTC"),

        "berkshire hathaway": (
            "Berkshire Hathaway",
            "BRK-B",
        ),

        "jpmorgan": ("JPMorgan Chase", "JPM"),
        "jpmorgan chase": ("JPMorgan Chase", "JPM"),
        "jpm": ("JPMorgan Chase", "JPM"),
    }

    RESEARCH_KEYWORDS = [
        "research",
        "rundown",
        "overview",
        "analyze",
        "analysis",
        "analysis of",
        "tell me about",
        "what is happening with",
        "what's happening with",
        "how is",
        "how's",
        "company",
        "company performance",
        "financial performance",
    ]

    MARKET_KEYWORDS = [
        "stock price",
        "share price",
        "current price",
        "market price",
        "price of",
        "stock doing",
        "shares doing",
        "trading at",
        "quote",
    ]

    NEWS_KEYWORDS = [
        "latest news",
        "recent news",
        "financial news",
        "market news",
        "news about",
        "news on",
        "what happened",
        "latest developments",
        "recent developments",
    ]

    GENERAL_FINANCE_KEYWORDS = [
        "ipo",
        "stock market",
        "mutual fund",
        "bond",
        "etf",
        "inflation",
        "interest rate",
        "dividend",
        "compound interest",
        "market capitalization",
        "market cap",
        "bull market",
        "bear market",
        "portfolio",
        "investment",
        "investing",
        "finance",
        "financial",
    ]

    @classmethod
    def _find_company(
        cls,
        message: str,
    ):

        normalized = message.lower().strip()

        # Check longer company names first
        company_names = sorted(
            cls.COMPANY_TICKERS.keys(),
            key=len,
            reverse=True,
        )

        for name in company_names:

            pattern = (
                r"(?<![a-z0-9])"
                + re.escape(name)
                + r"(?![a-z0-9])"
            )

            if re.search(
                pattern,
                normalized,
            ):
                company, ticker = (
                    cls.COMPANY_TICKERS[name]
                )

                return company, ticker

        return None, None

    @staticmethod
    def _contains_keyword(
        message: str,
        keywords: list[str],
    ) -> bool:

        normalized = message.lower()

        return any(
            keyword in normalized
            for keyword in keywords
        )

    def detect_intent(
        self,
        user_message: str,
    ) -> dict:

        message = user_message.strip()

        normalized = message.lower()

        company, ticker = self._find_company(
            message
        )

        # -----------------------------------------
        # 1. Company + market request
        # -----------------------------------------

        if (
            company
            and self._contains_keyword(
                message,
                self.MARKET_KEYWORDS,
            )
        ):
            return {
                "intent": "market_quote",
                "company": company,
                "ticker": ticker,
                "query": message,
            }

        # -----------------------------------------
        # 2. Company + news request
        # -----------------------------------------

        if (
            company
            and self._contains_keyword(
                message,
                self.NEWS_KEYWORDS,
            )
        ):
            return {
                "intent": "financial_news",
                "company": company,
                "ticker": ticker,
                "query": message,
            }

        # -----------------------------------------
        # 3. Company research
        # -----------------------------------------

        if company:

            return {
                "intent": "company_research",
                "company": company,
                "ticker": ticker,
                "query": message,
            }

        # -----------------------------------------
        # 4. Financial news without company
        # -----------------------------------------

        if self._contains_keyword(
            message,
            self.NEWS_KEYWORDS,
        ):
            return {
                "intent": "financial_news",
                "company": None,
                "ticker": None,
                "query": message,
            }

        # -----------------------------------------
        # 5. General finance
        # -----------------------------------------

        if self._contains_keyword(
            message,
            self.GENERAL_FINANCE_KEYWORDS,
        ):
            return {
                "intent": "general_finance",
                "company": None,
                "ticker": None,
                "query": message,
            }

        # -----------------------------------------
        # 6. General conversation
        # -----------------------------------------

        return {
            "intent": "general_conversation",
            "company": None,
            "ticker": None,
            "query": message,
        }