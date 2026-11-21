import unittest

import numpy as np
import pandas as pd

from src.pairs_finder import calculate_half_life, find_cointegrated_pairs
from src.trading_strategy import PairsTradingStrategy


def _ar1(n, phi, seed):
    rng = np.random.default_rng(seed)
    x = np.zeros(n)
    for t in range(1, n):
        x[t] = phi * x[t - 1] + rng.normal()
    return x


class HalfLifeTest(unittest.TestCase):
    def test_recovers_ar1_half_life(self):
        phi = 0.9
        expected = -np.log(2) / np.log(phi)
        self.assertAlmostEqual(calculate_half_life(_ar1(5000, phi, 0)), expected, delta=1.5)

    def test_random_walk_is_not_mean_reverting(self):
        walk = np.cumsum(np.random.default_rng(1).normal(size=2000))
        self.assertGreater(calculate_half_life(walk), 40)


class FindPairsTest(unittest.TestCase):
    def test_finds_cointegrated_pair_and_hedge_ratio(self):
        rng = np.random.default_rng(2)
        n = 1000
        b = np.cumsum(rng.normal(size=n)) + 100
        a = 2.0 * b + 5 + _ar1(n, 0.8, 3)
        c = np.cumsum(rng.normal(size=n)) + 100  # independent walk
        df = pd.DataFrame({"A": a, "B": b, "C": c})

        pairs = find_cointegrated_pairs(df)

        self.assertEqual([(p.stock1, p.stock2) for p in pairs], [("A", "B")])
        self.assertAlmostEqual(pairs[0].hedge_ratio, 2.0, delta=0.05)


class StrategyTest(unittest.TestCase):
    def _run(self, values, **kwargs):
        idx = pd.date_range("2024-01-01", periods=len(values))
        s = pd.Series(values, index=idx, dtype=float)
        return PairsTradingStrategy(**kwargs).run_segment(s, 0.0, 1.0, "A", "B")

    def test_short_spread_entry_and_mean_exit(self):
        trades = self._run([0, 2.5, 1.0, -0.5, 0])
        self.assertEqual(len(trades), 1)
        t = trades[0]
        self.assertEqual((t.entry_spread, t.exit_spread), (2.5, -0.5))
        self.assertAlmostEqual(t.pnl, 3.0)  # short spread profits when it falls

    def test_long_spread_entry_and_mean_exit(self):
        trades = self._run([0, -2.5, -1.0, 0.5])
        self.assertEqual(len(trades), 1)
        self.assertAlmostEqual(trades[0].pnl, 3.0)

    def test_stop_loss_closes_losing_position(self):
        trades = self._run([0, 2.5, 4.5])
        self.assertEqual(len(trades), 1)
        self.assertAlmostEqual(trades[0].pnl, -2.0)

    def test_no_trade_inside_entry_band(self):
        self.assertEqual(self._run([0, 1.0, -1.5, 1.9, 0]), [])


if __name__ == "__main__":
    unittest.main()
