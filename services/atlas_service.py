from services.intent_service import IntentService
from services.market_service import MarketService
from services.news_service import NewsService
from services.research_service import ResearchService
from services.ai_service import AIService


class AtlasService:

    def __init__(self):
        self.intent_service = IntentService()
        self.market_service = MarketService()
        self.news_service = NewsService()
        self.research_service = ResearchService()
        self.ai_service = AIService()

    def process_message(
        self,
        user_message: str,
        conversation_history: list | None = None,
    ) -> str:

        conversation_history = (
            conversation_history or []
        )

        # -----------------------------------------
        # 1. Detect intent
        # -----------------------------------------

        intent_result = (
            self.intent_service.detect_intent(
                user_message=user_message
            )
        )

        intent = intent_result.get(
            "intent"
        )

        company = intent_result.get(
            "company"
        )

        ticker = intent_result.get(
            "ticker"
        )

        # -----------------------------------------
        # 2. Financial news
        # -----------------------------------------

        if intent == "financial_news":

            try:
                articles = (
                    self.news_service
                    .search_financial_news(
                        page_size=5
                    )
                )

                if not articles:
                    return (
                        "📰 I couldn't find any "
                        "relevant financial news "
                        "right now."
                    )

                response = (
                    "📰 Latest Financial News\n\n"
                )

                for index, article in enumerate(
                    articles,
                    start=1,
                ):

                    title = (
                        article.get("title")
                        or "Untitled"
                    )

                    source = (
                        article.get("source")
                        or "Unknown source"
                    )

                    url = (
                        article.get("url")
                        or ""
                    )

                    response += (
                        f"{index}. {title}\n"
                        f"   Source: {source}\n"
                    )

                    if url:
                        response += (
                            f"   🔗 {url}\n"
                        )

                    response += "\n"

                return response.strip()

            except Exception as error:

                print(
                    f"NewsService error: {error}"
                )

                return (
                    "📰 I couldn't retrieve "
                    "the latest financial news "
                    "right now. Please try again."
                )

        # -----------------------------------------
        # 3. Company research
        # -----------------------------------------

        if intent == "company_research":

            if not company or not ticker:
                return (
                    "I couldn't identify the "
                    "company or ticker symbol. "
                    "Please try again with a "
                    "company name."
                )

            result = (
                self.research_service
                .research_company(
                    company_name=company,
                    symbol=ticker,
                    user_query=user_message,
                )
            )

            return self._format_company_research(
                result
            )

        # -----------------------------------------
        # 4. Market quote
        # -----------------------------------------

        if intent == "market_quote":

            if not ticker:
                return (
                    "Please provide a company "
                    "name or stock ticker."
                )

            try:

                quote = (
                    self.market_service
                    .get_quote(
                        symbol=ticker
                    )
                )

                if not quote:
                    return (
                        "I couldn't retrieve "
                        "the market quote right now."
                    )

                price = quote.get(
                    "price"
                )

                change = quote.get(
                    "change"
                )

                change_percent = quote.get(
                    "change_percent"
                )

                return (
                    f"📈 {company or ticker} "
                    f"({ticker})\n\n"
                    f"Price: ${price}\n"
                    f"Change: {change} "
                    f"({change_percent}%)"
                )

            except Exception as error:

                print(
                    f"MarketService error: {error}"
                )

                return (
                    "I couldn't retrieve the "
                    "market quote right now."
                )

        # -----------------------------------------
        # 5. General finance / conversation
        # -----------------------------------------

        try:

            response = (
                self.ai_service
                .generate_response(
                    prompt=user_message,
                    conversation_history=(
                        conversation_history
                    ),
                )
            )

            if response:
                return response

        except Exception as error:

            print(
                f"AIService error: {error}"
            )

        return (
            "📚 I can help with companies, "
            "stock prices, financial news, "
            "market questions, and financial "
            "concepts.\n\n"
            "Try asking something like:\n"
            "• What's happening with Apple?\n"
            "• What's Microsoft's stock price?\n"
            "• Show me the latest financial news\n"
            "• What is an IPO?"
        )

    # -----------------------------------------
    # Company research formatter
    # -----------------------------------------

    @staticmethod
    def _format_company_research(
        result: dict,
    ) -> str:

        company_name = (
            result.get("company_name")
            or result.get("company")
            or "Company"
        )

        ticker = (
            result.get("ticker")
            or result.get("symbol")
            or ""
        )

        market_data = (
            result.get("market_data")
            or {}
        )

        analysis = (
            result.get("analysis")
            or ""
        )

        sources = (
            result.get("sources")
            or []
        )

        response = (
            f"📊 {company_name}"
        )

        if ticker:
            response += (
                f" ({ticker})"
            )

        response += "\n\n"

        if market_data:

            price = market_data.get(
                "price"
            )

            change = market_data.get(
                "change"
            )

            change_percent = market_data.get(
                "change_percent"
            )

            if price is not None:
                response += (
                    f"Price: ${price}\n"
                )

            if change is not None:
                response += (
                    f"Change: {change} "
                )

            if change_percent is not None:
                response += (
                    f"({change_percent}%)"
                )

            response += "\n\n"

        if analysis:
            response += (
                f"{analysis}\n\n"
            )

        if sources:

            response += (
                "📰 Recent sources:\n"
            )

            for source in sources[:5]:

                if isinstance(
                    source,
                    dict,
                ):

                    title = (
                        source.get("title")
                        or "Untitled"
                    )

                    source_name = (
                        source.get("source")
                        or "Unknown source"
                    )

                    response += (
                        f"• {title} "
                        f"— {source_name}\n"
                    )

                else:

                    response += (
                        f"• {source}\n"
                    )

        return response.strip()