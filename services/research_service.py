from services.market_service import MarketService
from services.news_service import NewsService
from services.ai_service import AIService


class ResearchService:

    def __init__(self):
        self.market_service = MarketService()
        self.news_service = NewsService()
        self.ai_service = AIService()

    def research_company(
        self,
        company_name: str,
        symbol: str,
        user_query: str = "",
    ) -> dict:

        # -----------------------------------------
        # 1. Get market data
        # -----------------------------------------

        market_data = self.market_service.get_quote(
            symbol=symbol
        )

        # -----------------------------------------
        # 2. Get company-specific financial news
        # -----------------------------------------

        news = self.news_service.search_company_news(
            company_name=company_name,
            ticker=symbol,
            page_size=5,
        )

        # -----------------------------------------
        # 3. Prepare market information
        # -----------------------------------------

        market_text = (
            f"Company: {company_name}\n"
            f"Ticker: {symbol}\n"
            f"Price: "
            f"{market_data.get('price', 'N/A')}\n"
            f"Change: "
            f"{market_data.get('change', 'N/A')}\n"
            f"Change %: "
            f"{market_data.get('change_percent', 'N/A')}\n"
        )

        # -----------------------------------------
        # 4. Prepare news information
        # -----------------------------------------

        news_text = ""

        for index, article in enumerate(
            news,
            start=1,
        ):

            title = article.get(
                "title",
                "No title",
            )

            description = article.get(
                "description",
                "",
            )

            source = article.get(
                "source",
                "Unknown source",
            )

            published_at = article.get(
                "published_at",
                "",
            )

            news_text += (
                f"{index}. {title}\n"
                f"   Source: {source}\n"
                f"   Published: {published_at}\n"
                f"   Description: "
                f"{description}\n\n"
            )

        if not news_text:

            news_text = (
                "No recent financial news "
                "was found."
            )

        # -----------------------------------------
        # 5. Default user query
        # -----------------------------------------

        if not user_query:

            user_query = (
                f"Give me a quick financial "
                f"rundown on {company_name}."
            )

        # -----------------------------------------
        # 6. Build AI research prompt
        # -----------------------------------------

        prompt = f"""
You are Atlas, an AI Financial Assistant.

Analyze the following company using ONLY the
market data and news supplied below.

Company:
{company_name}

Ticker:
{symbol}

User request:
{user_query}

Market data:
{market_text}

Recent financial news:
{news_text}

Provide a concise financial overview.

Structure the response as:

1. Company overview
2. Current market performance
3. Recent developments
4. Key things investors should watch
5. Short conclusion

Important rules:

- Do not invent facts.
- Do not invent financial numbers.
- Clearly distinguish market data from analysis.
- Do not provide personalized investment advice.
- Mention when information is unavailable.
"""

        # -----------------------------------------
        # 7. Generate AI analysis
        # -----------------------------------------

        ai_response = self.ai_service.generate_response(
            user_message=prompt,
            conversation_history=[],
        )

        # -----------------------------------------
        # 8. Return complete research result
        # -----------------------------------------

        return {
            "company_name": company_name,
            "symbol": symbol,

            # Keep these aliases for compatibility
            "company": company_name,
            "ticker": symbol,

            "market_data": market_data,
            "market": market_data,

            "news": news,

            "analysis": ai_response,
        }