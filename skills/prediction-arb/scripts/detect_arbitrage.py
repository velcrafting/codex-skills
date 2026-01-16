# scripts/detect_arbitrage.py
#!/usr/bin/env python3
"""
Arbitrage Detector (Scout)
Compares Polymarket and Kalshi headline prices to find *candidate* discrepancies.

Important:
- This is a scouting tool. It is NOT an execution engine.
- It does not model slippage, depth, contract rule mismatches, or size constraints.
"""

import json
import os
from difflib import SequenceMatcher
from typing import Dict, List, Tuple

import pandas as pd

# Fee structures (approximate, adjustable via env)
POLYMARKET_FEE = float(os.getenv("POLYMARKET_FEE", "0.02"))  # 2%
KALSHI_FEE = float(os.getenv("KALSHI_FEE", "0.01"))  # 1%

# Similarity threshold (default 0.70)
MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", "0.70"))

POLY_PATH = os.getenv("POLYMARKET_IN", "polymarket_data.json")
KALSHI_PATH = os.getenv("KALSHI_IN", "kalshi_data.json")
OUT_CSV = os.getenv("ARB_OUT", "arbitrage_opportunities.csv")


def load_market_data() -> Tuple[List[Dict], List[Dict]]:
    """Load market data from JSON files."""
    with open(POLY_PATH, "r", encoding="utf-8") as f:
        polymarket = json.load(f)
    with open(KALSHI_PATH, "r", encoding="utf-8") as f:
        kalshi = json.load(f)
    return polymarket, kalshi


def normalize_event_name(name: str) -> str:
    """Normalize event name for matching."""
    return (
        name.lower()
        .strip()
        .replace("?", "")
        .replace("!", "")
        .replace(".", "")
        .replace(",", "")
    )


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()


def find_matching_events(poly_markets: List[Dict], kalshi_markets: List[Dict]) -> List[Dict]:
    """
    Find matching events across platforms using fuzzy string matching.

    Returns:
        List of matched event pairs
    """
    matches: List[Dict] = []

    for poly in poly_markets:
        poly_name = normalize_event_name(poly.get("event_name", ""))
        if not poly_name:
            continue

        for kal in kalshi_markets:
            kal_name = normalize_event_name(kal.get("event_name", ""))
            if not kal_name:
                continue

            score = similarity(poly_name, kal_name)
            if score >= MATCH_THRESHOLD:
                matches.append(
                    {
                        "polymarket": poly,
                        "kalshi": kal,
                        "similarity": score,
                        "event_name": poly.get("event_name", ""),
                    }
                )

    return matches


def calculate_arbitrage(
    poly_yes: float, poly_no: float, kalshi_yes: float, kalshi_no: float
) -> List[Dict]:
    """
    Calculate candidate arbitrage opportunities between two platforms.

    We include:
    - Cross-outcome "sum to $1" checks (theoretical)
    - Same-outcome spread checks (buy low, sell high) (theoretical)

    Returns:
        List of candidate opportunities.
    """
    opportunities: List[Dict] = []

    # Strategy A: Buy Polymarket YES + Buy Kalshi NO
    cost_a = poly_yes * (1 + POLYMARKET_FEE) + kalshi_no * (1 + KALSHI_FEE)
    if 0 < cost_a < 1.0:
        profit = 1.0 - cost_a
        opportunities.append(
            {
                "strategy": "Buy Polymarket YES + Buy Kalshi NO",
                "theoretical_cost": cost_a,
                "theoretical_return": 1.0,
                "theoretical_profit": profit,
                "profit_pct": (profit / cost_a) * 100 if cost_a else 0.0,
            }
        )

    # Strategy B: Buy Polymarket NO + Buy Kalshi YES
    cost_b = poly_no * (1 + POLYMARKET_FEE) + kalshi_yes * (1 + KALSHI_FEE)
    if 0 < cost_b < 1.0:
        profit = 1.0 - cost_b
        opportunities.append(
            {
                "strategy": "Buy Polymarket NO + Buy Kalshi YES",
                "theoretical_cost": cost_b,
                "theoretical_return": 1.0,
                "theoretical_profit": profit,
                "profit_pct": (profit / cost_b) * 100 if cost_b else 0.0,
            }
        )

    # Same-outcome spread check (YES)
    # If one venue offers meaningfully lower YES than the other (after fees), flag it.
    # NOTE: This assumes you could buy on one venue and sell/hedge on the other, which may not be feasible.
    if poly_yes > 0 and kalshi_yes > 0:
        # Buy Polymarket YES, "sell" Kalshi YES
        if poly_yes < kalshi_yes * (1 - KALSHI_FEE - POLYMARKET_FEE):
            profit = kalshi_yes - poly_yes - (poly_yes * POLYMARKET_FEE) - (kalshi_yes * KALSHI_FEE)
            if profit > 0:
                opportunities.append(
                    {
                        "strategy": "Buy Polymarket YES vs Kalshi YES (spread)",
                        "buy_price": poly_yes,
                        "sell_price": kalshi_yes,
                        "theoretical_profit": profit,
                        "profit_pct": (profit / poly_yes) * 100 if poly_yes else 0.0,
                    }
                )

        # Buy Kalshi YES, "sell" Polymarket YES
        if kalshi_yes < poly_yes * (1 - KALSHI_FEE - POLYMARKET_FEE):
            profit = poly_yes - kalshi_yes - (kalshi_yes * KALSHI_FEE) - (poly_yes * POLYMARKET_FEE)
            if profit > 0:
                opportunities.append(
                    {
                        "strategy": "Buy Kalshi YES vs Polymarket YES (spread)",
                        "buy_price": kalshi_yes,
                        "sell_price": poly_yes,
                        "theoretical_profit": profit,
                        "profit_pct": (profit / kalshi_yes) * 100 if kalshi_yes else 0.0,
                    }
                )

    return opportunities


def detect_arbitrage() -> pd.DataFrame:
    """Detect candidate opportunities and return a DataFrame sorted by profit_pct."""
    polymarket, kalshi = load_market_data()
    matches = find_matching_events(polymarket, kalshi)

    all_rows: List[Dict] = []

    for match in matches:
        poly = match["polymarket"]
        kal = match["kalshi"]

        # Polymarket uses yes_price/no_price
        poly_yes = float(poly.get("yes_price", 0) or 0)
        poly_no = float(poly.get("no_price", 0) or 0)

        # Kalshi script now exports yes_mid/no_mid; fall back if needed
        kal_yes = float(kal.get("yes_mid", kal.get("yes_price", 0)) or 0)
        kal_no = float(kal.get("no_mid", kal.get("no_price", 0)) or 0)

        if not (poly_yes and poly_no and kal_yes and kal_no):
            continue

        opportunities = calculate_arbitrage(poly_yes, poly_no, kal_yes, kal_no)

        for opp in opportunities:
            opp.update(
                {
                    "event_name": match.get("event_name", ""),
                    "match_similarity": match.get("similarity", 0.0),
                    "polymarket_yes": poly_yes,
                    "polymarket_no": poly_no,
                    "kalshi_yes": kal_yes,
                    "kalshi_no": kal_no,
                    "polymarket_fee": POLYMARKET_FEE,
                    "kalshi_fee": KALSHI_FEE,
                }
            )
            all_rows.append(opp)

    if not all_rows:
        return pd.DataFrame()

    df = pd.DataFrame(all_rows)
    df = df.sort_values("profit_pct", ascending=False)

    return df


def main() -> None:
    print("Analyzing candidate discrepancies...")

    df = detect_arbitrage()

    if df.empty:
        print("No candidate opportunities found.")
        return

    df.to_csv(OUT_CSV, index=False)
    print(f"Found {len(df)} candidates. Saved to {OUT_CSV}")

    print("\n=== TOP CANDIDATES ===\n")
    for _, row in df.head(5).iterrows():
        print(f"Event: {str(row.get('event_name',''))[:70]}...")
        print(f"Strategy: {row.get('strategy')}")
        profit = row.get("theoretical_profit", row.get("profit", 0))
        print(f"Theoretical profit: {float(profit):.4f} ({float(row.get('profit_pct', 0)):.2f}%)")
        print(
            f"Prices: Poly YES={row.get('polymarket_yes'):.3f}, NO={row.get('polymarket_no'):.3f} | "
            f"Kal YES={row.get('kalshi_yes'):.3f}, NO={row.get('kalshi_no'):.3f}"
        )
        print(f"Match similarity: {float(row.get('match_similarity', 0)):.2f}")
        print("-" * 60)


if __name__ == "__main__":
    main()
