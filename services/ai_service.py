from google import genai
from google.genai import errors

from config.settings import settings


class AIService:

    def __init__(self):

        self.client = None

        if settings.LLM_API_KEY:
            self.client = genai.Client(
                api_key=settings.LLM_API_KEY
            )

        self.model = "gemini-3.6-flash"

    def generate_response(
        self,
        user_message: str,
        conversation_history: list[dict] | None = None,
    ) -> str:

        conversation_history = (
            conversation_history or []
        )

        # -----------------------------------------
        # Try Gemini first
        # -----------------------------------------

        if self.client:

            try:

                history_text = ""

                for message in conversation_history[-10:]:

                    role = message.get(
                        "role",
                        "user",
                    )

                    content = message.get(
                        "message",
                        "",
                    )

                    history_text += (
                        f"{role}: {content}\n"
                    )

                prompt = f"""
You are Atlas, an AI Financial Assistant.

Provide a clear and concise financial response.

Do not invent financial facts.
Do not provide personalized investment advice.

Conversation history:

{history_text}

User request:

{user_message}
"""

                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt,
                    )
                )

                if response.text:
                    return response.text.strip()

            except errors.ClientError as error:

                print(
                    f"Gemini unavailable: {error}"
                )

            except Exception as error:

                print(
                    f"Gemini error: {error}"
                )

        # -----------------------------------------
        # Local fallback
        # -----------------------------------------

        return self._fallback_response(
            user_message
        )

    # ---------------------------------------------
    # Local fallback response
    # ---------------------------------------------

    @staticmethod
    def _fallback_response(
        user_message: str,
    ) -> str:

        text = user_message.lower()

        # -----------------------------------------
        # IPO
        # -----------------------------------------

        if "ipo" in text:

            return (
                "📚 IPO stands for Initial Public "
                "Offering.\n\n"
                "It is the process through which a "
                "private company offers its shares "
                "to the public for the first time "
                "and becomes publicly traded.\n\n"
                "Companies typically use an IPO to "
                "raise capital for growth, expansion, "
                "debt reduction, or other business "
                "purposes."
            )

        # -----------------------------------------
        # Greeting
        # -----------------------------------------

        greetings = [
            "hello",
            "hi",
            "hey",
            "hello atlas",
            "hi atlas",
            "hey atlas",
        ]

        if text.strip() in greetings:

            return (
                "👋 Hello! I'm Atlas, your AI "
                "Financial Assistant.\n\n"
                "I can help you with:\n"
                "• Company research\n"
                "• Stock prices\n"
                "• Financial news\n"
                "• Market information\n"
                "• Financial concepts"
            )

        # -----------------------------------------
        # Generic fallback
        # -----------------------------------------

        return (
            "I can currently retrieve financial "
            "market data and recent financial news, "
            "but my advanced AI analysis service is "
            "temporarily unavailable.\n\n"
            "Please try a company name, stock ticker, "
            "market question, or financial concept."
        )