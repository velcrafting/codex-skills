# scripts/fetch_polymarket.py
#!/usr/bin/env python3
"""
Polymarket Data Fetcher (Public)
Fetches current market metadata + prices from Polymarket CLOB endpoints (best-effort).

Outputs: polymarket_data.json (list[dict])

Notes:
- Polymarket endpoints and response shapes can drift. This script prints response
  snippets on error to make debugging fast.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

import requests

DEFAULT_POLYMARKET_BASE_URL = "https://clob.polymarket.com"


def _base_url() -> str:
    return os.getenv("POLYMARKET_BASE_URL", DEFAULT_POLYMARKET_BASE_URL).rstrip("/")


def fetch_polymarket_markets(active: bool = True, limit: int = 50) -> List[Dict]:
    """
    Fetch active markets from Polymarket.

    This uses a commonly seen /markets endpoint. If Polymarket changes it,
    the error output will help you update paths/params quickly.
    """
    url = f"{_base_url()}/markets"
    params = {"active": "true" if active else "false"}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        # Some APIs return {"markets":[...]} while others return [...]
        if isinstance(payload, dict) and "markets" in payload:
            markets = payload.get("markets", [])
        else:
            markets = payload if isinstance(payload, list) else []
        return markets[:limit]
    except requests.RequestException as e:
        body = ""
        try:
            body = resp.text[:500]  # type: ignore[name-defined]
        except Exception:
            pass
        print(f"Error fetching Polymarket markets: {e}")
        if body:
            print(f"Response: {body}")
        return []


def fetch_polymarket_prices(condition_id: str) -> Optional[Dict]:
    """
    Fetch current YES/NO prices for a specific market/condition.

    Uses a commonly seen /prices endpoint. If this endpoint differs, you can
    swap it to /price, /midpoint, or /book-based logic later.
    """
    url = f"{_base_url()}/prices"
    params = {"market": condition_id}
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        payload = resp.json()
        return payload if isinstance(payload, dict) else None
    except requests.RequestException as e:
        body = ""
        try:
            body = resp.text[:500]  # type: ignore[name-defined]
        except Exception:
            pass
        print(f"Error fetching Polymarket prices for {condition_id}: {e}")
        if body:
            print(f"Response: {body}")
        return None


def get_polymarket_data(limit: int = 50) -> List[Dict]:
    """
    Fetch and normalize Polymarket data for analysis.

    Returns a list of dicts with:
    - event_name (question)
    - yes_price, no_price (floats 0..1)
    - condition_id
    """
    markets = fetch_polymarket_markets(active=True, limit=limit)
    now = datetime.now().isoformat()
    results: List[Dict] = []

    for market in markets:
        condition_id = market.get("condition_id") or market.get("id")
        if not condition_id:
            continue

        prices = fetch_polymarket_prices(condition_id)
        if not prices:
            continue

        # Best-effort extraction of YES/NO
        yes = prices.get("yes", 0) if isinstance(prices, dict) else 0
        no = prices.get("no", 0) if isinstance(prices, dict) else 0

        try:
            yes_f = float(yes)
            no_f = float(no)
        except (TypeError, ValueError):
            continue

        results.append(
            {
                "platform": "Polymarket",
                "event_name": market.get("question", "Unknown"),
                "condition_id": condition_id,
                "yes_price": yes_f,
                "no_price": no_f,
                "volume": market.get("volume", 0),
                "fetched_at": now,
            }
        )

    return results


def main() -> None:
    limit = int(os.getenv("POLYMARKET_FETCH_LIMIT", "50"))
    out_path = os.getenv("POLYMARKET_OUT", "polymarket_data.json")

    print(f"Fetching Polymarket data from {_base_url()} (limit={limit}) ...")
    data = get_polymarket_data(limit=limit)

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(data)} markets to {out_path}")


if __name__ == "__main__":
    main()
