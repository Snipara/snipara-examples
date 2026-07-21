from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "benchmarks" / "hosted-context-2026-06" / "verify_results.py"
CONTINUITY_RESULTS_PATH = ROOT / "proof" / "project-continuity-2026-07" / "results.json"
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

    def test_continuity_summary_group_aggregates_match_models(self) -> None:
        with CONTINUITY_RESULTS_PATH.open(encoding="utf-8") as handle:
            results = json.load(handle)

        models = results["continuity_suite"]["models"]
        expected = {
            row["runtime_group"]: row
            for row in results["continuity_suite"]["group_aggregates"]
        }
        for runtime_group, aggregate in expected.items():
            group = [row for row in models if row["runtime_group"] == runtime_group]
            self.assertEqual(sum(row["cold_passes"] for row in group), aggregate["cold_passes"])
            self.assertEqual(
                sum(row["snipara_passes"] for row in group), aggregate["snipara_passes"]
            )
            self.assertEqual(sum(row["total_runs"] for row in group), aggregate["total_runs"])

        self.assertFalse(results["limits"]["negative_control_published"])


if __name__ == "__main__":
    unittest.main()
