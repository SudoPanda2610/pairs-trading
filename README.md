![Pairs Trading banner](assets/banner.svg)

# Pairs Trading

A statistical-arbitrage research framework for identifying cointegrated assets and testing mean-reversion strategies.

## Method

Candidate pairs are evaluated with the Engle-Granger procedure:

1. Estimate a hedge relationship with ordinary least squares.
2. Test the residual spread for stationarity.
3. Measure mean-reversion strength with the Hurst exponent.
4. Trade standardized spread deviations with explicit entry, exit, and stop rules.

The backtester records positions, trade-level PnL, total return, Sharpe ratio, drawdown, and win rate.

## Run

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Useful experiment modes:

```bash
python run.py --days 500 --stocks 20 --threshold 2.5
python run.py --sensitivity
python -m unittest -v
```

## Repository layout

```text
src/pairs_finder.py       Cointegration and Hurst diagnostics
src/trading_strategy.py   Signal and position rules
src/backtest.py           Portfolio and trade accounting
run.py                    Experiment entry point
test_real_data.py         Real-data integration checks
backtest_trades.csv       Recorded trade ledger
```

## Research scope

Cointegration is estimated from finite historical samples and can break under structural change. Reported backtests do not include every execution cost, borrow constraint, or capacity limit required for live deployment.
