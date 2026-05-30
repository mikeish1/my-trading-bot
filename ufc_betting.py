"""
UFC/MMA Betting Module - Advanced Fight Analysis
"""

def get_ufc_picks(bankroll=1000, risk_level="moderate", bet_type="all"):
    """
    Get UFC fight picks with AI analysis and Kelly sizing
    """
    # UFC Fight Card (replace with real API data)
    fights = [
        {
            "fight": "Alex Pereira vs Jamahal Hill",
            "fighter_a": {"name": "Alex Pereira", "odds": -150, "confidence": 72, "edge": 8.5, "record": "11-2", "style": "Muay Thai/Kickboxing"},
            "fighter_b": {"name": "Jamahal Hill", "odds": +130, "confidence": 28, "edge": 2.1, "record": "12-1", "style": "Kickboxing"},
            "weight_class": "Light Heavyweight",
            "event": "UFC 307",
            "date": "2026-06-15"
        },
        {
            "fight": "Sean O'Malley vs Merab Dvalishvili",
            "fighter_a": {"name": "Sean O'Malley", "odds": +180, "confidence": 58, "edge": 6.2, "record": "18-2", "style": "Striker"},
            "fighter_b": {"name": "Merab Dvalishvili", "odds": -220, "confidence": 42, "edge": 3.8, "record": "18-4", "style": "Wrestling/Pressure"},
            "weight_class": "Bantamweight",
            "event": "UFC 307",
            "date": "2026-06-15"
        },
        {
            "fight": "Islam Makhachev vs Dustin Poirier",
            "fighter_a": {"name": "Islam Makhachev", "odds": -280, "confidence": 75, "edge": 9.2, "record": "26-1", "style": "Sambo/Wrestling"},
            "fighter_b": {"name": "Dustin Poirier", "odds": +220, "confidence": 25, "edge": 1.5, "record": "29-8", "style": "Boxing/BJJ"},
            "weight_class": "Lightweight",
            "event": "UFC 308",
            "date": "2026-06-22"
        }
    ]
    
    recommendations = []
    remaining_bankroll = bankroll
    
    for fight in fights:
        # Analyze both fighters
        for fighter_key in ["fighter_a", "fighter_b"]:
            fighter = fight[fighter_key]
            
            if fighter["edge"] < 4.0:
                continue
            
            # Kelly Criterion
            decimal_odds = abs(fighter["odds"]) / 100 if fighter["odds"] < 0 else 100 / fighter["odds"]
            win_prob = fighter["confidence"] / 100
            kelly_fraction = (decimal_odds * win_prob - (1 - win_prob)) / decimal_odds
            
            # Risk adjustment
            if risk_level == "conservative":
                kelly_fraction *= 0.5
            elif risk_level == "aggressive":
                kelly_fraction *= 1.5
            
            # Cap at 5% of bankroll
            bet_size = min(kelly_fraction * bankroll, bankroll * 0.05)
            bet_size = max(bet_size, 25)
            
            if bet_size <= remaining_bankroll:
                recommendations.append({
                    "fight": fight["fight"],
                    "pick": fighter["name"],
                    "opponent": fight["fighter_b"]["name"] if fighter_key == "fighter_a" else fight["fighter_a"]["name"],
                    "weight_class": fight["weight_class"],
                    "event": fight["event"],
                    "date": fight["date"],
                    "odds": fighter["odds"],
                    "confidence": fighter["confidence"],
                    "edge": fighter["edge"],
                    "style": fighter["style"],
                    "record": fighter["record"],
                    "bet_size": round(bet_size, 2),
                    "expected_value": round(bet_size * (fighter["edge"] / 100), 2),
                    "bet_type": "Moneyline"
                })
                remaining_bankroll -= bet_size
    
    # Sort by edge
    recommendations.sort(key=lambda x: x["edge"], reverse=True)
    
    return {
        "bankroll": bankroll,
        "total_bet": round(sum(r["bet_size"] for r in recommendations), 2),
        "expected_profit": round(sum(r["expected_value"] for r in recommendations), 2),
        "num_bets": len(recommendations),
        "recommendations": recommendations[:5]  # Top 5
    }

def get_fight_props(bankroll=500):
    """
    Get prop bet recommendations (method of victory, round, etc.)
    """
    props = [
        {
            "fight": "Pereira vs Hill",
            "prop": "Pereira by KO/TKO",
            "odds": +180,
            "confidence": 55,
            "edge": 5.8
        },
        {
            "fight": "O'Malley vs Dvalishvili",
            "prop": "Fight goes to Decision",
            "odds": -130,
            "confidence": 68,
            "edge": 6.5
        }
    ]
    
    recommendations = []
    remaining = bankroll
    
    for prop in props:
        decimal_odds = abs(prop["odds"]) / 100 if prop["odds"] < 0 else 100 / prop["odds"]
        win_prob = prop["confidence"] / 100
        kelly = (decimal_odds * win_prob - (1 - win_prob)) / decimal_odds
        bet_size = min(kelly * bankroll, bankroll * 0.03)
        bet_size = max(bet_size, 20)
        
        if bet_size <= remaining:
            recommendations.append({
                "fight": prop["fight"],
                "prop": prop["prop"],
                "odds": prop["odds"],
                "confidence": prop["confidence"],
                "edge": prop["edge"],
                "bet_size": round(bet_size, 2),
                "expected_value": round(bet_size * (prop["edge"] / 100), 2)
            })
            remaining -= bet_size
    
    return recommendations
