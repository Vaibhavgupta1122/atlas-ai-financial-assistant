import requests

from config.settings import settings


class NewsService:

    BASE_URL = "https://newsapi.org/v2/everything"

    @staticmethod
    def search_news(
        query: str,
        page_size: int = 20,
    ) -> list[dict]:

        if not settings.NEWS_API_KEY:
            raise ValueError(
                "NEWS_API_KEY is missing from the .env file."
            )

        params = {
            "q": query,
            "apiKey": settings.NEWS_API_KEY,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": page_size,
        }

        response = requests.get(
            NewsService.BASE_URL,
            params=params,
            timeout=15,
        )

        response.raise_for_status()

        data = response.json()

        articles = data.get("articles", [])

        results = []

        for article in articles:

            title = article.get("title")

            if not title:
                continue

            results.append(
                {
                    "title": title,
                    "description": article.get(
                        "description"
                    ),
                    "source": (
                        article.get(
                            "source",
                            {}
                        ).get("name")
                    ),
                    "url": article.get("url"),
                    "published_at": article.get(
                        "publishedAt"
                    ),
                }
            )

        return results

    @staticmethod
    def search_company_news(
        company_name: str,
        ticker: str | None = None,
        page_size: int = 5,
    ) -> list[dict]:

        company_name = company_name.strip()

        # -----------------------------------------
        # Build search terms
        # -----------------------------------------

        search_terms = [
            f'"{company_name}"'
        ]

        if ticker:
            search_terms.append(
                f'"{ticker}"'
            )

        company_query = " OR ".join(
            search_terms
        )

        query = (
            f"({company_query}) AND "
            "(stock OR shares OR earnings OR "
            "revenue OR profit OR market OR "
            "financial OR investor OR investment "
            "OR guidance)"
        )

        # -----------------------------------------
        # Get larger candidate set
        # -----------------------------------------

        articles = NewsService.search_news(
            query=query,
            page_size=30,
        )

        company_lower = company_name.lower()

        ticker_lower = (
            ticker.lower()
            if ticker
            else None
        )

        relevant_articles = []

        # -----------------------------------------
        # Relevance scoring
        # -----------------------------------------

        for article in articles:

            title = (
                article.get("title")
                or ""
            )

            description = (
                article.get("description")
                or ""
            )

            text = (
                f"{title} {description}"
            ).lower()

            score = 0

            # Strongest signal: exact company name
            if company_lower in text:
                score += 5

            # Ticker signal
            if (
                ticker_lower
                and ticker_lower in text
            ):
                score += 4

            # Financial relevance
            financial_keywords = [
                "stock",
                "shares",
                "earnings",
                "revenue",
                "profit",
                "market",
                "financial",
                "investor",
                "investment",
                "guidance",
                "quarter",
                "forecast",
                "valuation",
            ]

            for keyword in financial_keywords:
                if keyword in text:
                    score += 1

            if score >= 5:
                relevant_articles.append(
                    (
                        score,
                        article,
                    )
                )

        # -----------------------------------------
        # Highest relevance first
        # -----------------------------------------

        relevant_articles.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        # -----------------------------------------
        # Remove duplicate titles
        # -----------------------------------------

        results = []

        seen_titles = set()

        for score, article in relevant_articles:

            title = (
                article.get("title")
                or ""
            )

            normalized_title = (
                title.strip().lower()
            )

            if normalized_title in seen_titles:
                continue

            seen_titles.add(
                normalized_title
            )

            results.append(article)

            if len(results) >= page_size:
                break

        return results

    @staticmethod
    def search_financial_news(
        page_size: int = 5,
    ) -> list[dict]:

        query = (
            "stock market OR stocks OR "
            "earnings OR IPO OR markets OR "
            "Wall Street OR Nasdaq OR NYSE OR "
            "investing OR financial markets"
        )

        articles = NewsService.search_news(
            query=query,
            page_size=30,
        )

        results = []

        financial_keywords = [
            "stock",
            "stocks",
            "market",
            "markets",
            "earnings",
            "revenue",
            "profit",
            "shares",
            "investor",
            "investing",
            "ipo",
            "nasdaq",
            "nyse",
            "wall street",
            "financial",
            "economy",
            "fed",
            "interest rate",
        ]

        for article in articles:

            title = (
                article.get("title")
                or ""
            )

            description = (
                article.get("description")
                or ""
            )

            text = (
                f"{title} {description}"
            ).lower()

            score = sum(
                1
                for keyword in financial_keywords
                if keyword in text
            )

            if score >= 1:
                results.append(
                    (
                        score,
                        article,
                    )
                )

        results.sort(
            key=lambda item: item[0],
            reverse=True,
        )

        final_results = []

        seen_titles = set()

        for score, article in results:

            title = (
                article.get("title")
                or ""
            )

            normalized_title = (
                title.strip().lower()
            )

            if normalized_title in seen_titles:
                continue

            seen_titles.add(
                normalized_title
            )

            final_results.append(article)

            if len(final_results) >= page_size:
                break

        return final_results