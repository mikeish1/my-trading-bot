"""
Railway Deployment Entry Point
V2 Single-Table Trading Intelligence System
"""

from scripts.advanced_portfolio_analyzer import generate_master_recommendation
import os

if __name__ == "__main__":
    # Default ticker - change this to your preferred stock
    ticker = os.environ.get("DEFAULT_TICKER", "NVDA")
    
    print(f"🚀 Running Trading System for {ticker}")
    print("=" * 50)
    
    result = generate_master_recommendation(ticker, capital=25000)
    
    print("\n📊 RECOMMENDATION:")
    print(f"Ticker: {result.get('ticker')}")
    print(f"Score: {result.get('composite_score')}/10")
    print(f"Recommendation: {result.get('recommendation')}")
    print(f"Position Size: {result.get('recommended_position_size_pct')}%")
    print(f"Regime: {result.get('current_regime')}")
    print(f"VIX: {result.get('current_vix')}")
    print(f"Deep RL Action: {result.get('deep_rl_action')}")
    print("=" * 50)