import numpy as np
import pandas as pd
import statsmodels.tsa.stattools as ts
from dataclasses import dataclass
from typing import List


@dataclass
class PairStats:
    stock1: str
    stock2: str
    hedge_ratio: float
    p_value: float
    half_life: float
    spread_mean: float
    spread_std: float


def calculate_half_life(spread: np.ndarray) -> float:
    """Calculate half-life of mean reversion using OLS on lagged spread."""
    spread_lag = np.roll(spread, 1)
    spread_ret = spread - spread_lag
    spread_ret = spread_ret[1:]
    spread_lag = spread_lag[1:]

    # Regression: d(spread) ~ theta * spread_lag
    X = spread_lag
    y = spread_ret
    try:
        res = np.linalg.lstsq(X[:, None], y, rcond=None)
        theta = res[0][0]
        if theta >= 0:
            return np.inf  # not mean-reverting
        return -np.log(2) / theta
    except np.linalg.LinAlgError:
        return np.inf


def find_cointegrated_pairs(
    data: pd.DataFrame,
    p_threshold: float = 0.05,
) -> List[PairStats]:
    """Identify pairs that are cointegrated (p_value < threshold)."""
    n = data.shape[1]
    keys = data.columns
    pairs = []

    for i in range(n):
        for j in range(i + 1, n):
            s1 = data.iloc[:, i]
            s2 = data.iloc[:, j]

            # OLS hedge ratio; ADF on residuals for stationarity
            try:
                X = np.vstack([s2, np.ones(len(s2))]).T
                beta, alpha = np.linalg.lstsq(X, s1, rcond=None)[0]
                spread = s1 - beta * s2 - alpha
                p_value = ts.adfuller(spread)[1]

                if p_value < p_threshold:
                    hl = calculate_half_life(spread)
                    if 1 <= hl <= 40:
                        pairs.append(PairStats(
                            stock1=keys[i],
                            stock2=keys[j],
                            hedge_ratio=beta,
                            p_value=p_value,
                            half_life=hl,
                            spread_mean=float(np.mean(spread)),
                            spread_std=float(np.std(spread)),
                        ))
            except Exception:
                continue

    # Sort by strongest cointegration (lowest p-value)
    pairs.sort(key=lambda x: x.p_value)
    return pairs
