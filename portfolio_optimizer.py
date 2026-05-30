"""
Portfolio Optimizer & Exit Logic Module
Adds capital-constrained optimization and exit signals
WITHOUT modifying existing functions
"""

from advanced_portfolio_analyzer import generate_master_recommendation, detect_regime_and_adjust
import numpy as np

def optimize_portfolio_for_capital(available_capital, max_position_pct=3.0, risk_tolerance=1.0, num_picks=5):
    """
    Capital-Constrained Portfolio Optimizer
    Selects optimal trades to maximize profit within capital limit
    """
    # High-potential tickers to analyze
    tickers = ["NVDA", "SMCI", "AMD", "AVGO", "TSLA", "META", "AAPL", "MSFT", "GOOGL", "AMZN", "AMD", "QCOM", "INTC", "CRM", "ADBE"]
    
    recommendations = []
    
    for ticker in tickers:
        try:
            rec = generate_master_recommendation(ticker, capital=available_capital)
            if rec["status"] == "Success" and rec["composite_score"] >= 6.0:
                # Calculate profit potential score
                profit_score = rec["composite_score"] * rec.get("recommended_position_size_pct", 1.0)
                recommendations.append({
                    "ticker": ticker,
                    "score": rec["composite_score"],
                    "profit_potential": round(profit_score, 2),
                    "expected_return_pct": round(rec["composite_score"] * 2.2, 1),
                    "position_pct": min(rec["recommended_position_size_pct"], max_position_pct),
                    "regime": rec["current_regime"],
                    "vix": rec["current_vix"],
                    "exit_trailing_stop": 8.0 if "High VIX" in rec["current_regime"] else 6.0,
                    "profit_target_1": 15.0,
                    "profit_target_2": 25.0,
                    "time_stop_days": 12,
                    "action": rec["recommendation"],
                    "deep_rl_action": rec.get("deep_rl_action", "Hold")
                })
        except:
            continue
    
    # Sort by profit potential
    recommendations.sort(key=lambda x: x["profit_potential"], reverse=True)
    
    # Select top N within capital constraint
    selected = []
    remaining_capital = available_capital
    
    for rec in recommendations:
        position_value = available_capital * (rec["position_pct"] / 100)
        
        if position_value <= remaining_capital and len(selected) < num_picks:
            rec["allocated_capital"] = round(position_value, 2)
            rec["allocated_pct"] = round((position_value / available_capital) * 100, 1)
            selected.append(rec)
            remaining_capital -= position_value
    
    # Calculate portfolio metrics
    total_allocated = sum(s["allocated_capital"] for s in selected)
    expected_portfolio_return = sum(s["expected_return_pct"] * s["allocated_pct"] / 100 for s in selected)
    
    return {
        "available_capital": available_capital,
        "total_allocated": round(total_allocated, 2),
        "cash_reserve": round(remaining_capital, 2),
        "num_positions": len(selected),
        "expected_portfolio_return_pct": round(expected_portfolio_return, 1),
        "expected_profit_usd": round(total_allocated * expected_portfolio_return / 100, 2),
        "risk_level": "MODERATE" if expected_portfolio_return > 12 else "CONSERVATIVE",
        "positions": selected
    }

def get_exit_signal(ticker, current_price, entry_price, peak_price, days_held, current_regime, composite_score):
    """
    Exit Signal System - Tells you when to exit positions
    """
    signals = []
    action = "HOLD"
    urgency = "LOW"
    
    # Calculate returns
    current_return = ((current_price - entry_price) / entry_price) * 100
    peak_return = ((peak_price - entry_price) / entry_price) * 100
    trailing_stop_distance = ((peak_price - current_price) / peak_price) * 100
    
    # 1. Trailing Stop Check
    trailing_stop_pct = 8.0 if "High VIX" in current_regime else 6.0
    if trailing_stop_distance >= trailing_stop_pct:
        signals.append(f"🔴 TRAILING STOP HIT - Down {trailing_stop_distance:.1f}% from peak")
        action = "EXIT"
        urgency = "HIGH"
    
    # 2. Profit Target Check
    if current_return >= 25:
        signals.append(f"🟢 PROFIT TARGET 2 HIT (+{current_return:.1f}%) - Consider scaling out 50%")
        action = "SCALE OUT"
        urgency = "MEDIUM"
    elif current_return >= 15:
        signals.append(f"🟡 PROFIT TARGET 1 HIT (+{current_return:.1f}%) - Consider taking partial profits")
        action = "SCALE OUT"
        urgency = "LOW"
    
    # 3. Regime Change Check
    if "High VIX" in current_regime and current_return > 0:
        signals.append(f"🟠 REGIME SHIFT - Market turning bearish, consider reducing position")
        action = "REDUCE"
        urgency = "MEDIUM"
    
    # 4. Time Stop Check
    if days_held >= 12 and current_return < 5:
        signals.append(f"⏰ TIME STOP - {days_held} days held with only +{current_return:.1f}% return")
        action = "EXIT"
        urgency = "MEDIUM"
    
    # 5. Score Deterioration
    if composite_score < 5.0 and current_return > 0:
        signals.append(f"📉 SCORE DETERIORATION - Composite score dropped to {composite_score}/10")
        action = "REDUCE"
        urgency = "LOW"
    
    if not signals:
        signals.append(f"✅ HOLD - All conditions favorable (+{current_return:.1f}% return)")
    
    return {
        "action": action,
        "urgency": urgency,
        "current_return_pct": round(current_return, 1),
        "trailing_stop_distance_pct": round(trailing_stop_distance, 1),
        "signals": signals,
        "days_held": days_held
    }
