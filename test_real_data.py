"""
Smoke test against real prices (needs network access for yfinance).

Run directly:
    python test_real_data.py
"""

from src.backtest import RollingWindowBacktest
from src.data_loader import download_stock_data


def main():
    # Sector peers that are plausible cointegration candidates
    energy_stocks = ['XOM', 'CVX', 'COP', 'SLB']
    consumer_stocks = ['KO', 'PEP', 'WMT', 'TGT']
    tickers = energy_stocks + consumer_stocks

    data = download_stock_data(tickers, '2023-01-01', '2024-01-01')

    backtester = RollingWindowBacktest(data, formation_period=60, trading_period=20)
    backtester.run()
    backtester.get_summary()

    if backtester.results:
        print("\nOK: found pairs and executed trades.")
    else:
        print("\nNo trades executed. Try different stocks or a longer period.")


if __name__ == "__main__":
    main()
