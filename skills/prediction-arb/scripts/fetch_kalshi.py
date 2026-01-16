# scripts/fetch_kalshi.py
#!/usr/bin/env python3
"""
Kalshi Data Fetcher (Public)
Fetches current open market quotes from Kalshi Trade API v2.

Outputs: kalshi_data.json (list[dict])
"""

import json
import os
from datetime import datetime
from typing import Dict, List

import requests

# Official (elections) base used in Kalshi OpenAPI docs
DEFAULT_KALSHI_BASE_URL = "https://api.elections.kalshi.com/trade-api/v2"


def _base_url() -> str:
    return os.getenv("KALSHI_BASE_URL", DEFAULT_KALSHI_BASE_URL).rstrip("/")


def fetch_kalshi_markets(limit: int = 50) -> List[Dict]:
    """
    Fetch open markets from Kalshi (public).

    Returns the raw 'markets' array (best-effort).
    """
    url = f"{_base_url()}/markets"
    params = {"status": "open", "limit": str(limit)}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        return payload.get("markets", []) if isinstance(payload, dict) else []
    except requests.RequestException as e:
        # Print response body if available for easier debugging.
        body = ""
        try:
            body = resp.text[:500]  # type: ignore[name-defined]
        except Exception:
            pass
        print(f"Error fetching Kalshi markets: {e}")
        if body:
            print(f"Response: {body}")
        return []


def get_kalshi_data(limit: int = 50) -> List[Dict]:
    """
    Fetch and normalize Kalshi data for analysis.

    Notes:
    - Kalshi quotes are in cents (0-100). We normalize to dollars (0.00-1.00).
    - We preserve bid/ask for YES/NO and also compute midpoints if both sides exist.
    """
    markets = fetch_kalshi_markets(limit=limit)
    now = datetime.now().isoformat()
    results: List[Dict] = []

    for m in markets:
        ticker = m.get("ticker")
        if not ticker:
            continue

        # Convert cents -> dollars (0..1)
        yes_bid = (m.get("yes_bid") or 0) / 100
        yes_ask = (m.get("yes_ask") or 0) / 100
        no_bid = (m.get("no_bid") or 0) / 100
        no_ask = (m.get("no_ask") or 0) / 100

        yes_mid = (yes_bid + yes_ask) / 2 if yes_bid and yes_ask else 0.0
        no_mid = (no_bid + no_ask) / 2 if no_bid and no_ask else 0.0

        results.append(
            {
                "platform": "Kalshi",
                "event_name": m.get("title", "Unknown"),
                "ticker": ticker,
                "yes_bid": float(yes_bid),
                "yes_ask": float(yes_ask),
                "no_bid": float(no_bid),
                "no_ask": float(no_ask),
                "yes_mid": float(yes_mid),
                "no_mid": float(no_mid),
                "volume": m.get("volume", 0),
                "open_interest": m.get("open_interest", 0),
                "close_time": m.get("close_time"),
                "fetched_at": now,
            }
        )

    return results


def main() -> None:
    limit = int(os.getenv("KALSHI_FETCH_LIMIT", "50"))
    out_path = os.getenv("KALSHI_OUT", "kalshi_data.json")

    print(f"Fetching Kalshi data from {_base_url()} (limit={limit}) ...")
    data = get_kalshi_data(limit=limit)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} markets to {out_path}")


if __name__ == "__main__":
    main()
