"""
Quick test with known good pairs
"""

# Run this to test:
# python test_real_data.py

import numpy as np
from src.backtest import run_pairs_backtest, print_results

print("Testing with sector-specific stocks that should be cointegrated...")
print()

# Test energy sector (very likely to be cointegrated)
energy_stocks = ['XOM', 'CVX', 'COP', 'SLB']

# Test consumer staples (also likely cointegrated)
consumer_stocks = ['KO', 'PEP', 'WMT', 'TGT']

# Combine
tickers = energy_stocks + consumer_stocks

results = run_pairs_backtest(
    tickers=tickers,
    use_real_data=True,
    start_date='2023-01-01',
    end_date='2024-01-01',
    entry_threshold=1.5,  # More aggressive to get more trades
    lookback=40,  # Shorter lookback = more responsive
    verbose=True
)

print_results(results)

if results.num_trades > 0:
    print("\n✅ SUCCESS! Found pairs and executed trades!")
    print("Use these results on your resume!")
else:
    print("\n⚠️ No trades executed. Try different stocks or time period.")
    print("Suggestion: Try --start 2022-01-01 --end 2024-01-01 for longer period")