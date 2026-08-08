from services.atlas_service import AtlasService


def main():

    atlas = AtlasService()

    test_messages = [
        "Give me a quick rundown on Apple",
        "What's happening with Nvidia?",
        "What is an IPO?",
    ]

    for message in test_messages:

        print("\n")
        print("=" * 70)
        print("USER:")
        print(message)
        print("=" * 70)

        response = atlas.process_message(
            user_message=message,
            conversation_history=[],
        )

        print("\nATLAS:")
        print(response)


if __name__ == "__main__":
    main()