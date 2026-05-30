"""
Automated Test Suite for V2 Trading System
Run this to validate all components are working correctly.
"""

import sys
from datetime import datetime
import traceback

# Test Results Storage
test_results = {
    "passed": [],
    "failed": [],
    "errors": []
}

def log_test(name, passed, error=None):
    if passed:
        test_results["passed"].append(name)
        print(f"✅ PASS: {name}")
    else:
        test_results["failed"].append(name)
        test_results["errors"].append((name, error))
        print(f"❌ FAIL: {name}")
        if error:
            print(f"   Error: {error}")

def run_test_suite():
    print("=" * 60)
    print("🚀 V2 TRADING SYSTEM - AUTOMATED TEST SUITE")
    print(f"Started: {datetime.now()}")
    print("=" * 60)
    
    # Test 1: Core Module Import
    try:
        from advanced_portfolio_analyzer import generate_master_recommendation
        log_test("Core Module Import", True)
    except Exception as e:
        log_test("Core Module Import", False, str(e))
        return  # Can't continue without core module
    
    # Test 2: Master Recommendation Function
    try:
        result = generate_master_recommendation("NVDA", capital=25000)
        assert result["status"] == "Success"
        assert "composite_score" in result
        assert "recommendation" in result
        assert result["composite_score"] >= 0 and result["composite_score"] <= 10
        log_test("Master Recommendation Function", True)
    except Exception as e:
        log_test("Master Recommendation Function", False, str(e))
    
    # Test 3: Regime Detection
    try:
        from advanced_portfolio_analyzer import detect_regime_and_adjust
        regime_result = detect_regime_and_adjust(["NVDA", "AAPL"], capital=25000)
        assert "current_regime" in regime_result or "error" in regime_result
        log_test("Regime Detection", True)
    except Exception as e:
        log_test("Regime Detection", False, str(e))
    
    # Test 4: Dynamic Position Sizing
    try:
        from advanced_portfolio_analyzer import calculate_dynamic_position_size
        sizing = calculate_dynamic_position_size(
            win_rate=0.58, reward_risk_ratio=2.5,
            current_regime="Neutral / Choppy", vrp=5.0
        )
        assert "recommended_position_size_pct" in sizing
        assert sizing["recommended_position_size_pct"] > 0
        log_test("Dynamic Position Sizing", True)
    except Exception as e:
        log_test("Dynamic Position Sizing", False, str(e))
    
    # Test 5: Multi-Factor Ensemble
    try:
        from advanced_portfolio_analyzer import calculate_multi_factor_ensemble
        ensemble = calculate_multi_factor_ensemble(
            rl_recommendation="Increase",
            current_regime="Neutral / Choppy",
            vrp="Rich Premium",
            monte_carlo_sharpe=3.5,
            base_sharpe=3.8,
            use_real_sentiment=False
        )
        assert "composite_score" in ensemble
        assert 0 <= ensemble["composite_score"] <= 10
        log_test("Multi-Factor Ensemble", True)
    except Exception as e:
        log_test("Multi-Factor Ensemble", False, str(e))
    
    # Test 6: Deep RL Agent
    try:
        from advanced_portfolio_analyzer import DeepRLTradingAgent
        agent = DeepRLTradingAgent()
        state = agent.get_state(
            regime="Neutral / Choppy", vix=20.0, vrp=5.0,
            recent_return=0.01, sentiment=0.6, sharpe=3.5,
            drawdown=-0.03, capital_utilization=0.65
        )
        action = agent.act(state)
        assert action in [0, 1, 2, 3]  # Valid actions
        log_test("Deep RL Agent", True)
    except Exception as e:
        log_test("Deep RL Agent", False, str(e))
    
    # Test 7: Error Handling (Invalid Ticker)
    try:
        result = generate_master_recommendation("INVALID_TICKER_XYZ", capital=1000)
        # Should either succeed with fallback or return error status
        assert result["status"] in ["Success", "Error"]
        log_test("Error Handling (Invalid Ticker)", True)
    except Exception as e:
        log_test("Error Handling (Invalid Ticker)", False, str(e))
    
    # Test 8: Output Structure Validation
    try:
        result = generate_master_recommendation("AAPL", capital=50000)
        required_fields = [
            "ticker", "composite_score", "recommendation",
            "recommended_position_size_pct", "current_regime",
            "current_vix", "deep_rl_action", "bear_market_adjustment"
        ]
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
        log_test("Output Structure Validation", True)
    except Exception as e:
        log_test("Output Structure Validation", False, str(e))
    
    # Print Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"✅ Passed: {len(test_results['passed'])}")
    print(f"❌ Failed: {len(test_results['failed'])}")
    print(f"📈 Success Rate: {len(test_results['passed'])/(len(test_results['passed'])+len(test_results['failed']))*100:.1f}%")
    
    if test_results['failed']:
        print("\n❌ FAILED TESTS:")
        for name, error in test_results['errors']:
            print(f"  - {name}: {error}")
    
    print("\n" + "=" * 60)
    return len(test_results['failed']) == 0

if __name__ == "__main__":
    success = run_test_suite()
    sys.exit(0 if success else 1)
