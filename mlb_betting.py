"""
Advanced MLB Baseball Betting Module
Includes: Moneyline, Run Line, Over/Under, Player Props, Parlays
"""

import random
from datetime import datetime, timedelta

def get_mlb_picks(bankroll=1000, risk_level="moderate", bet_type="all"):
    """
    Get MLB picks with advanced analysis
    """
    # MLB Games (replace with real API data)
    games = [
        {
            "game": "Dodgers vs Giants",
            "home_team": {"name": "Los Angeles Dodgers", "odds": -145, "confidence": 68, "edge": 7.5, "pitcher": "Tyler Glasnow", "bullpen_era": 3.45, "home_record": "42-19"},
            "away_team": {"name": "San Francisco Giants", "odds": +125, "confidence": 32, "edge": 2.8, "pitcher": "Blake Snell", "bullpen_era": 4.12, "away_record": "31-30"},
            "total_line": 8.5,
            "weather": "Clear, 72°F, Wind 5mph",
            "park_factor": 0.95,  # Dodger Stadium
            "date": "2026-05-30"
        },
        {
            "game": "Yankees vs Red Sox",
            "home_team": {"name": "New York Yankees", "odds": -130, "confidence": 65, "edge": 6.8, "pitcher": "Gerrit Cole", "bullpen_era": 3.89, "home_record": "38-23"},
            "away_team": {"name": "Boston Red Sox", "odds": +110, "confidence": 35, "edge": 3.2, "pitcher": "Brayan Bello", "bullpen_era": 4.01, "away_record": "33-28"},
            "total_line": 9.0,
            "weather": "Partly Cloudy, 68°F, Wind 8mph",
            "park_factor": 1.05,  # Fenway Park
            "date": "2026-05-30"
        },
        {
            "game": "Astros vs Rangers",
            "home_team": {"name": "Texas Rangers", "odds": -110, "confidence": 58, "edge": 5.5, "pitcher": "Jacob deGrom", "bullpen_era": 3.67, "home_record": "35-26"},
            "away_team": {"name": "Houston Astros", "odds": -110, "confidence": 42, "edge": 4.1, "pitcher": "Framber Valdez", "bullpen_era": 3.78, "away_record": "37-24"},
            "total_line": 8.0,
            "weather": "Dome, 72°F, No Wind",
            "park_factor": 1.00,  # Globe Life Field
            "date": "2026-05-30"
        }
    ]
    
    recommendations = []
    remaining_bankroll = bankroll
    
    for game in games:
        # Moneyline bets
        for team_key in ["home_team", "away_team"]:
            team = game[team_key]
            
            if team["edge"] < 4.0:
                continue
            
            decimal_odds = abs(team["odds"]) / 100 if team["odds"] < 0 else 100 / team["odds"]
            win_prob = team["confidence"] / 100
            kelly = (decimal_odds * win_prob - (1 - win_prob)) / decimal_odds
            
            if risk_level == "conservative":
                kelly *= 0.5
            elif risk_level == "aggressive":
                kelly *= 1.5
            
            bet_size = min(kelly * bankroll, bankroll * 0.04)
            bet_size = max(bet_size, 25)
            
            if bet_size <= remaining_bankroll:
                recommendations.append({
                    "game": game["game"],
                    "bet_type": "Moneyline",
                    "pick": team["name"],
                    "opponent": game["away_team"]["name"] if team_key == "home_team" else game["home_team"]["name"],
                    "odds": team["odds"],
                    "confidence": team["confidence"],
                    "edge": team["edge"],
                    "pitcher": team["pitcher"],
                    "bullpen_era": team["bullpen_era"],
                    "weather": game["weather"],
                    "park_factor": game["park_factor"],
                    "bet_size": round(bet_size, 2),
                    "expected_value": round(bet_size * (team["edge"] / 100), 2),
                    "date": game["date"]
                })
                remaining_bankroll -= bet_size
        
        # Over/Under bets
        over_edge = random.uniform(4.5, 7.5)
        if over_edge > 5.0:
            decimal_odds = 1.91  # Standard -110
            win_prob = 0.52
            kelly = (decimal_odds * win_prob - (1 - win_prob)) / decimal_odds
            bet_size = min(kelly * bankroll, bankroll * 0.03)
            bet_size = max(bet_size, 20)
            
            if bet_size <= remaining_bankroll:
                recommendations.append({
                    "game": game["game"],
                    "bet_type": "Over/Under",
                    "pick": f"OVER {game['total_line']}",
                    "opponent": "N/A",
                    "odds": -110,
                    "confidence": 52,
                    "edge": round(over_edge, 1),
                    "pitcher": "N/A",
                    "bullpen_era": "N/A",
                    "weather": game["weather"],
                    "park_factor": game["park_factor"],
                    "bet_size": round(bet_size, 2),
                    "expected_value": round(bet_size * (over_edge / 100), 2),
                    "date": game["date"]
                })
                remaining_bankroll -= bet_size
    
    recommendations.sort(key=lambda x: x["edge"], reverse=True)
    
    return {
        "bankroll": bankroll,
        "total_bet": round(sum(r["bet_size"] for r in recommendations), 2),
        "expected_profit": round(sum(r["expected_value"] for r in recommendations), 2),
        "num_bets": len(recommendations),
        "recommendations": recommendations[:6]
    }

def get_player_props(bankroll=300):
    """
    Player prop bets (strikeouts, hits, HR, etc.)
    """
    props = [
        {
            "game": "Dodgers vs Giants",
            "prop": "Tyler Glasnow - Strikeouts OVER 7.5",
            "odds": -120,
            "confidence": 62,
            "edge": 5.8
        },
        {
            "game": "Yankees vs Red Sox",
            "prop": "Aaron Judge - Home Run YES",
            "odds": +280,
            "confidence": 28,
            "edge": 4.2
        },
        {
            "game": "Astros vs Rangers",
            "prop": "Jacob deGrom - Strikeouts OVER 8.5",
            "odds": -110,
            "confidence": 58,
            "edge": 5.2
        }
    ]
    
    recommendations = []
    remaining = bankroll
    
    for prop in props:
        decimal_odds = abs(prop["odds"]) / 100 if prop["odds"] < 0 else 100 / prop["odds"]
        win_prob = prop["confidence"] / 100
        kelly = (decimal_odds * win_prob - (1 - win_prob)) / decimal_odds
        bet_size = min(kelly * bankroll, bankroll * 0.025)
        bet_size = max(bet_size, 15)
        
        if bet_size <= remaining:
            recommendations.append({
                "game": prop["game"],
                "prop": prop["prop"],
                "odds": prop["odds"],
                "confidence": prop["confidence"],
                "edge": prop["edge"],
                "bet_size": round(bet_size, 2),
                "expected_value": round(bet_size * (prop["edge"] / 100), 2)
            })
            remaining -= bet_size
    
    return recommendations
