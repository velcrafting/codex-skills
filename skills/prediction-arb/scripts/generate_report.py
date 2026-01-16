#!/usr/bin/env python3
"""
Arbitrage Report Generator
Creates a formatted report of candidate arbitrage opportunities.

Notes:
- This tool is scouting-oriented. Reported profits are theoretical.
- It expects the CSV produced by detect_arbitrage.py (which may use
  'theoretical_profit' instead of 'profit').
"""

from datetime import datetime

import pandas as pd


def generate_report(
    csv_path: str = "arbitrage_opportunities.csv",
    out_path: str = "arbitrage_report.md",
) -> str | None:
    """Generate a markdown report of candidate arbitrage opportunities."""
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"No {csv_path} found. Run detection first.")
        return None

    if df.empty:
        print(f"{csv_path} is empty. No candidates to report.")
        return None

    # Prefer theoretical fields if present
    profit_col = "theoretical_profit" if "theoretical_profit" in df.columns else "profit"
    profit_pct_col = "profit_pct" if "profit_pct" in df.columns else None

    best_profit_pct = df[profit_pct_col].max() if profit_pct_col else float("nan")
    avg_profit_pct = df[profit_pct_col].mean() if profit_pct_col else float("nan")

    report = f"""# Candidate Arbitrage Opportunities Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Markets Compared**: Polymarket vs Kalshi

## Summary

- **Total Candidates Found**: {len(df)}
- **Best Theoretical Profit %**: {best_profit_pct:.2f}%{" (missing profit_pct column)" if not profit_pct_col else ""}
- **Average Theoretical Profit %**: {avg_profit_pct:.2f}%{" (missing profit_pct column)" if not profit_pct_col else ""}

## Top Candidates

| Event | Strategy | Theoretical Profit | Profit % |
|-------|----------|--------------------|----------|
"""

    # Sort by profit_pct when available, else by profit
    if profit_pct_col:
        df_sorted = df.sort_values(profit_pct_col, ascending=False)
    else:
        df_sorted = df.sort_values(profit_col, ascending=False)

    for _, row in df_sorted.head(10).iterrows():
        event_name = str(row.get("event_name", "Unknown"))
        event = event_name[:40] + "..." if len(event_name) > 40 else event_name
        strategy = str(row.get("strategy", "Unknown"))
        profit = float(row.get(profit_col, 0) or 0)
        profit_pct = float(row.get(profit_pct_col, 0) or 0) if profit_pct_col else 0.0

        report += f"| {event} | {strategy} | ${profit:.4f} | {profit_pct:.2f}% |\n"

    report += """
## Risk Warnings

1. **Execution Risk**: Prices may change before any action is taken
2. **Liquidity Risk**: You may not be able to fill size at quoted prices
3. **Rule Risk**: Settlement rules may differ between platforms for seemingly similar markets
4. **Fee Risk**: Fees, spreads, and effective costs can change without notice
5. **Match Risk**: Fuzzy matching can produce false positives

## Recommended Actions

1. Verify the match and settlement rules manually before acting
2. Confirm orderbook depth and spreads (especially on the execution venue)
3. Start with small size and record fill quality vs quoted prices
4. Track lead/lag behavior over time, not just point-in-time discrepancies

---
*This report is informational only and reflects theoretical calculations, not guaranteed outcomes.*
"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"Report saved to {out_path}")
    return report


if __name__ == "__main__":
    generate_report()
