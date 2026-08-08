from services.research_service import ResearchService


def main():

    research_service = ResearchService()

    result = research_service.research_company(
        symbol="AAPL",
        company_name="Apple",
    )

    print("\n================================")
    print("ATLAS COMPANY RESEARCH")
    print("================================")

    print(
        f"\nCompany: "
        f"{result['company_name']}"
    )

    print(
        f"Ticker: "
        f"{result['symbol']}"
    )

    print("\nMarket Data:")
    print(
        result["market_data"]
    )

    print("\nAnalysis:")
    print(
        result["analysis"]
    )

    print("\nSources:")

    for article in result["news"]:
        print(
            f"- {article['title']} "
            f"({article['source']})"
        )


if __name__ == "__main__":
    main()