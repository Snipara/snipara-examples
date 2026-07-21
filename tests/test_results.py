from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "benchmarks" / "hosted-context-2026-06" / "verify_results.py"
SPEC = importlib.util.spec_from_file_location("verify_results", VERIFY_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("could not load benchmark verifier")
VERIFY_RESULTS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VERIFY_RESULTS)


class ResultsTest(unittest.TestCase):
    def test_frozen_results_are_internally_consistent(self) -> None:
        case_count, quality_delta, window_reduction = VERIFY_RESULTS.verify()
        self.assertEqual(case_count, 12)
        self.assertAlmostEqual(quality_delta, 0.854167, places=6)
        self.assertAlmostEqual(window_reduction, 80.26, places=2)


if __name__ == "__main__":
    unittest.main()

