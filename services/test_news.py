from services.news_service import NewsService


def main():

    articles = NewsService.search_news(
        query="NVIDIA",
        page_size=5,
    )

    print("\nLatest NVIDIA News:\n")

    for index, article in enumerate(
        articles,
        start=1,
    ):
        print(f"\n--- Article {index} ---")

        print(
            f"Title: {article['title']}"
        )

        print(
            f"Source: {article['source']}"
        )

        print(
            f"Published: {article['published_at']}"
        )

        print(
            f"URL: {article['url']}"
        )


if __name__ == "__main__":
    main()