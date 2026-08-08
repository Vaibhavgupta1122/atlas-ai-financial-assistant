from services.ai_service import AIService


def main():
    ai = AIService()

    response = ai.generate_response(
        user_message="What is an IPO?",
        conversation_history=[],
    )

    print("\nAtlas:\n")
    print(response)


if __name__ == "__main__":
    main()