![Pairs Trading banner](assets/banner.svg)

# Pairs Trading

A statistical-arbitrage research framework for identifying cointegrated assets and testing mean-reversion strategies.

## Method

Candidate pairs are evaluated with the Engle-Granger procedure:

1. Estimate a hedge relationship with ordinary least squares.
2. Test the residual spread for stationarity.
3. Keep pairs whose mean-reversion half-life (AR(1) fit of the spread) is between 1 and 40 days.
4. Trade standardized spread deviations with explicit entry, exit, and stop rules.

The backtester walks forward (60-day formation, 20-day trading windows), trades the lowest-p-value pair in each window using spread parameters fixed from the formation period, and reports trade count, total PnL, win rate, and average PnL.

## Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Tests (offline, synthetic data):

```bash
python -m unittest -v
```

Network smoke test against real prices (needs `yfinance` access):

```bash
python test_real_data.py
```

## Repository layout

```text
src/pairs_finder.py       Cointegration and half-life diagnostics
src/trading_strategy.py   Signal and position rules
src/backtest.py           Walk-forward backtest and trade summary
src/data_loader.py        yfinance price download
tests/test_core.py        Offline unit tests
run.py                    Experiment entry point
test_real_data.py         Real-data integration checks
backtest_trades.csv       Recorded trade ledger
```

## Research scope

Cointegration is estimated from finite historical samples and can break under structural change. Reported backtests do not include every execution cost, borrow constraint, or capacity limit required for live deployment.
