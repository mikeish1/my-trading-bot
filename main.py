from advanced_portfolio_analyzer import generate_master_recommendation
import os

if __name__ == "__main__":
    ticker = os.environ.get("DEFAULT_TICKER", "NVDA")
    result = generate_master_recommendation(ticker, capital=25000)
    print(result)
