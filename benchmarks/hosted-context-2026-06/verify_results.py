#!/usr/bin/env python3
"""Verify the frozen public benchmark evidence with the standard library."""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
CASES_PATH = ROOT / "cases.json"
RESULTS_PATH = ROOT / "results.json"
METRICS = (
    "overall",
    "correctness",
    "faithfulness",
    "true_hallucination_rate",
    "factual_accuracy",
)


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def mean(values: list[float]) -> float:
    if not values:
        raise AssertionError("cannot average an empty metric set")
    return sum(values) / len(values)


def assert_close(actual: float, expected: float, *, label: str, tolerance: float = 1e-6) -> None:
    if not math.isclose(actual, expected, rel_tol=0.0, abs_tol=tolerance):
        raise AssertionError(f"{label}: expected {expected}, computed {actual}")


def verify() -> tuple[int, float, float]:
    case_manifest = load_json(CASES_PATH)
    results = load_json(RESULTS_PATH)

    digest = hashlib.sha256(CASES_PATH.read_bytes()).hexdigest()
    if results["case_manifest_sha256"] != digest:
        raise AssertionError(
            "cases.json hash mismatch: update results.json only after reviewing the changed cases"
        )

    manifest_ids = [case["id"] for case in case_manifest["cases"]]
    result_ids = [case["id"] for case in results["cases"]]
    if len(manifest_ids) != len(set(manifest_ids)):
        raise AssertionError("cases.json contains duplicate case IDs")
    if manifest_ids != result_ids:
        raise AssertionError("results.json case order or coverage differs from cases.json")
    if results["run"]["case_count"] != len(result_ids):
        raise AssertionError("reported case_count differs from committed results")

    computed: dict[str, dict[str, float]] = {}
    for cohort in ("with_snipara", "raw_window"):
        computed[cohort] = {}
        for metric in METRICS:
            value = mean([float(case[cohort][metric]) for case in results["cases"]])
            computed[cohort][metric] = value
            tolerance = 0.001 if metric in {"true_hallucination_rate", "factual_accuracy"} else 1e-6
            assert_close(
                value,
                float(results["aggregates"][cohort][metric]),
                label=f"{cohort}.{metric}",
                tolerance=tolerance,
            )

    deltas = results["aggregates"]["deltas"]
    for metric in ("overall", "correctness", "faithfulness", "factual_accuracy"):
        assert_close(
            computed["with_snipara"][metric] - computed["raw_window"][metric],
            float(deltas[metric]),
            label=f"deltas.{metric}",
            tolerance=0.001,
        )
    assert_close(
        computed["raw_window"]["true_hallucination_rate"]
        - computed["with_snipara"]["true_hallucination_rate"],
        float(deltas["true_hallucination_rate_reduction"]),
        label="deltas.true_hallucination_rate_reduction",
        tolerance=0.001,
    )

    context = results["context"]
    full_reduction = (1 - context["mean_snipara_tokens"] / context["full_docs_tokens"]) * 100
    window_reduction = (
        1 - context["mean_snipara_tokens"] / context["baseline_context_tokens"]
    ) * 100
    assert_close(full_reduction, context["full_reduction_pct"], label="full_reduction_pct", tolerance=0.01)
    assert_close(
        window_reduction,
        context["window_reduction_pct"],
        label="window_reduction_pct",
        tolerance=0.01,
    )

    return len(result_ids), float(deltas["overall"]), float(context["window_reduction_pct"])


def main() -> None:
    case_count, quality_delta, window_reduction = verify()
    print(
        f"verified {case_count} cases: quality {quality_delta:+.3f}, "
        f"window tokens -{window_reduction:.2f}%"
    )


if __name__ == "__main__":
    main()
