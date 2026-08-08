from services.intent_service import IntentService


def main():

    intent_service = IntentService()

    test_messages = [
        "Give me a quick rundown on Apple",
        "What's happening with Nvidia?",
        "What is Microsoft's stock price?",
        "Show me the latest financial news",
        "What is an IPO?",
        "Hello Atlas",
    ]

    for message in test_messages:

        result = intent_service.detect_intent(
            message
        )

        print("\nUser:")
        print(message)

        print("\nDetected intent:")
        print(result)

        print("-" * 60)


if __name__ == "__main__":
    main()