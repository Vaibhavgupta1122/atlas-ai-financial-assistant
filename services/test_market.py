from services.market_service import MarketService


def main():

    result = MarketService.get_quote("AAPL")

    print("\nMarket Data:\n")

    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()